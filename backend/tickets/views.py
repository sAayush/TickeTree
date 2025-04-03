from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import Ticket, TicketTransaction
from .serializers import (
    TicketSerializer, TicketBookingSerializer,
    TicketVerificationSerializer, TicketTransactionSerializer,
    QRCodeVerificationSerializer, TicketTransferSerializer
)
from .services import BlockchainService, QRCodeService
from utils.utils import create_response
from movies.models import Show

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

    @action(detail=False, methods=['post'])
    def book(self, request):
        serializer = TicketBookingSerializer(data=request.data)
        if not serializer.is_valid():
            return create_response(
                status="error",
                message="Invalid booking data",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        show = Show.objects.get(id=data['show_id'])
        blockchain_service = BlockchainService()
        tickets = []
        transactions = []

        for seat_number in data['seat_numbers']:
            # Mint ticket on blockchain
            blockchain_result = blockchain_service.mint_ticket(
                data['user_wallet_address'],
                show.id,
                seat_number,
                show.price
            )

            if not blockchain_result['success']:
                return create_response(
                    status="error",
                    message="Failed to mint ticket on blockchain",
                    data=blockchain_result['error'],
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Create ticket in database
            ticket = Ticket.objects.create(
                user=request.user,
                show=show,
                seat_number=seat_number,
                price=show.price,
                token_id=blockchain_result['token_id'],
                transaction_hash=blockchain_result['transaction_hash']
            )

            # Generate QR code
            qr_result = ticket.generate_qr_code()
            if not qr_result['success']:
                return create_response(
                    status="error",
                    message="Failed to generate QR code",
                    data=qr_result['error'],
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            tickets.append(ticket)

            # Create transaction record
            transaction = TicketTransaction.objects.create(
                ticket=ticket,
                transaction_type='purchase',
                amount=show.price,
                blockchain_transaction_hash=blockchain_result['transaction_hash']
            )
            transactions.append(transaction)

        return create_response(
            status="success",
            message="Tickets booked successfully",
            data={
                'tickets': TicketSerializer(tickets, many=True).data,
                'transactions': TicketTransactionSerializer(transactions, many=True).data
            },
            status_code=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        ticket = self.get_object()
        if not ticket.qr_code:
            result = ticket.generate_qr_code()
            if not result['success']:
                return create_response(
                    status="error",
                    message="Failed to generate QR code",
                    data=result['error'],
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return create_response(
            status="success",
            message="QR code retrieved successfully",
            data={
                'qr_code': ticket.qr_code,
                'ticket_data': ticket.qr_data
            }
        )

    @action(detail=False, methods=['post'])
    def verify_qr(self, request):
        serializer = QRCodeVerificationSerializer(data=request.data)
        if not serializer.is_valid():
            return create_response(
                status="error",
                message="Invalid QR code data",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        qr_service = QRCodeService()
        verification_result = qr_service.verify_qr_code(serializer.validated_data['qr_data'])
        
        if not verification_result['success']:
            return create_response(
                status="error",
                message="Invalid QR code",
                data=verification_result['error'],
                status_code=status.HTTP_400_BAD_REQUEST
            )

        ticket_data = verification_result['ticket_data']
        try:
            ticket = Ticket.objects.get(
                token_id=ticket_data['token_id'],
                show_id=ticket_data['show_id'],
                seat_number=ticket_data['seat_number']
            )
        except Ticket.DoesNotExist:
            return create_response(
                status="error",
                message="Ticket not found",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # Verify ticket on blockchain
        blockchain_result = ticket.verify_on_blockchain()
        if not blockchain_result['success']:
            return create_response(
                status="error",
                message="Failed to verify ticket on blockchain",
                data=blockchain_result['error'],
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return create_response(
            status="success",
            message="Ticket verified successfully",
            data={
                'ticket': TicketSerializer(ticket).data,
                'is_valid': not ticket.is_used
            }
        )

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        ticket = self.get_object()
        serializer = TicketVerificationSerializer(data=request.data)
        
        if not serializer.is_valid():
            return create_response(
                status="error",
                message="Invalid verification data",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        if data['user_wallet_address'] != request.user.wallet_address:
            return create_response(
                status="error",
                message="Invalid wallet address",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        result = ticket.verify_on_blockchain()
        if not result['success']:
            return create_response(
                status="error",
                message="Failed to verify ticket on blockchain",
                data=result['error'],
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return create_response(
            status="success",
            message="Ticket verified successfully",
            data=TicketSerializer(ticket).data
        )

    @action(detail=True, methods=['post'])
    def use(self, request, pk=None):
        ticket = self.get_object()
        
        if ticket.is_used:
            return create_response(
                status="error",
                message="Ticket already used",
                status_code=status.HTTP_400_BAD_REQUEST
            )

        success, message = ticket.use_ticket()
        if not success:
            return create_response(
                status="error",
                message=message,
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return create_response(
            status="success",
            message="Ticket used successfully",
            data=TicketSerializer(ticket).data
        )

    @action(detail=False, methods=['post'])
    def transfer(self, request):
        serializer = TicketTransferSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return create_response(
                status="error",
                message="Invalid transfer data",
                data=serializer.errors,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data
        ticket = Ticket.objects.get(id=data['ticket_id'])
        
        # Transfer ticket
        success, message = ticket.transfer_ticket(data['new_owner_wallet_address'])
        if not success:
            return create_response(
                status="error",
                message=message,
                status_code=status.HTTP_400_BAD_REQUEST
            )

        # Create transaction record
        TicketTransaction.objects.create(
            ticket=ticket,
            transaction_type='transfer',
            amount=0,  # Transfer is free
            blockchain_transaction_hash=ticket.transfer_history[-1]['transaction_hash']
        )

        return create_response(
            status="success",
            message="Ticket transferred successfully",
            data=TicketSerializer(ticket).data
        )

    @action(detail=True, methods=['get'])
    def transfer_history(self, request, pk=None):
        ticket = self.get_object()
        return create_response(
            status="success",
            message="Transfer history retrieved successfully",
            data={
                'transfers': ticket.transfer_history
            }
        )

class TicketTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketTransaction.objects.all()
    serializer_class = TicketTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(ticket__user=self.request.user)
