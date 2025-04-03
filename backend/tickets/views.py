from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Ticket, TicketTransaction
from .serializers import TicketSerializer, TicketTransactionSerializer, TicketPurchaseSerializer
from web3 import Web3
import json
import os
from django.utils import timezone

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def purchase(self, request, pk=None):
        ticket = self.get_object()
        
        # Connect to blockchain
        w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_RPC_URL')))
        contract_address = os.getenv('TICKET_CONTRACT_ADDRESS')
        contract_abi = json.loads(os.getenv('TICKET_CONTRACT_ABI'))
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        try:
            # Purchase ticket on blockchain
            tx_hash = contract.functions.purchaseTicket(
                ticket.event.id if ticket.event else ticket.movie.id,
                ticket.show.id if ticket.show else 0,
                0 if ticket.ticket_type == 'movie' else 1,  # TicketType enum
                int(ticket.price * 10**18),  # Convert to wei
                ticket.seat_number
            ).transact({'from': request.user.wallet_address, 'value': int(ticket.price * 10**18)})
            
            # Wait for transaction receipt
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Update ticket with blockchain info
            ticket.blockchain_ticket_id = receipt['logs'][0]['topics'][1].hex()
            ticket.blockchain_transaction_hash = tx_hash.hex()
            ticket.status = 'confirmed'
            ticket.save()
            
            # Create transaction record
            TicketTransaction.objects.create(
                ticket=ticket,
                transaction_type='purchase',
                amount=ticket.price,
                blockchain_transaction_hash=tx_hash.hex()
            )
            
            return Response({'status': 'success', 'transaction_hash': tx_hash.hex()})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def use(self, request, pk=None):
        ticket = self.get_object()
        
        if ticket.status != 'confirmed':
            return Response({'error': 'Ticket is not confirmed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Connect to blockchain
        w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_RPC_URL')))
        contract_address = os.getenv('TICKET_CONTRACT_ADDRESS')
        contract_abi = json.loads(os.getenv('TICKET_CONTRACT_ABI'))
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        try:
            # Mark ticket as used on blockchain
            tx_hash = contract.functions.useTicket(
                int(ticket.blockchain_ticket_id, 16)
            ).transact({'from': request.user.wallet_address})
            
            # Update ticket status
            ticket.status = 'used'
            ticket.used_at = timezone.now()
            ticket.save()
            
            return Response({'status': 'success', 'transaction_hash': tx_hash.hex()})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        ticket = self.get_object()
        
        if ticket.status != 'confirmed':
            return Response({'error': 'Ticket is not confirmed'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Connect to blockchain
        w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_RPC_URL')))
        contract_address = os.getenv('TICKET_CONTRACT_ADDRESS')
        contract_abi = json.loads(os.getenv('TICKET_CONTRACT_ABI'))
        contract = w3.eth.contract(address=contract_address, abi=contract_abi)
        
        try:
            # Process refund on blockchain
            tx_hash = contract.functions.refundTicket(
                int(ticket.blockchain_ticket_id, 16)
            ).transact({'from': request.user.wallet_address})
            
            # Update ticket status
            ticket.status = 'refunded'
            ticket.cancelled_at = timezone.now()
            ticket.save()
            
            # Create transaction record
            TicketTransaction.objects.create(
                ticket=ticket,
                transaction_type='refund',
                amount=ticket.price,
                blockchain_transaction_hash=tx_hash.hex()
            )
            
            return Response({'status': 'success', 'transaction_hash': tx_hash.hex()})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TicketTransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TicketTransaction.objects.all()
    serializer_class = TicketTransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(ticket__user=self.request.user)
