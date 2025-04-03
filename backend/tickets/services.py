from web3 import Web3
import os
from django.conf import settings
import json
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
import base64

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv('BLOCKCHAIN_RPC_URL')))
        self.contract_address = os.getenv('TICKET_CONTRACT_ADDRESS')
        self.private_key = os.getenv('PRIVATE_KEY')
        
        # Load contract ABI
        with open('blockchain/artifacts/contracts/Ticket.sol/Ticket.json') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
        
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )

    def mint_ticket(self, user_address, show_id, seat_number, price):
        try:
            # Create transaction
            nonce = self.w3.eth.get_transaction_count(self.w3.eth.default_account)
            transaction = self.contract.functions.mintTicket(
                user_address,
                show_id,
                seat_number,
                price
            ).build_transaction({
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })

            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=self.private_key
            )

            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            # Get token ID from event
            event = self.contract.events.TicketMinted().process_receipt(tx_receipt)[0]
            token_id = event.args.tokenId

            return {
                'success': True,
                'token_id': token_id,
                'transaction_hash': tx_hash.hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def verify_ticket(self, token_id):
        try:
            ticket_info = self.contract.functions.getTicketInfo(token_id).call()
            return {
                'success': True,
                'show_id': ticket_info[0],
                'seat_number': ticket_info[1],
                'price': ticket_info[2],
                'is_used': ticket_info[3],
                'timestamp': ticket_info[4]
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def use_ticket(self, token_id, user_address):
        try:
            nonce = self.w3.eth.get_transaction_count(user_address)
            transaction = self.contract.functions.useTicket(token_id).build_transaction({
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })

            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=self.private_key
            )

            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            return {
                'success': True,
                'transaction_hash': tx_hash.hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def transfer_ticket(self, token_id, from_address, to_address):
        try:
            # Check if the ticket exists and belongs to the sender
            owner = self.contract.functions.ownerOf(token_id).call()
            if owner.lower() != from_address.lower():
                return {
                    'success': False,
                    'error': 'You are not the owner of this ticket'
                }

            # Create transfer transaction
            nonce = self.w3.eth.get_transaction_count(from_address)
            transaction = self.contract.functions.transferFrom(
                from_address,
                to_address,
                token_id
            ).build_transaction({
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': self.w3.eth.gas_price
            })

            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(
                transaction,
                private_key=self.private_key
            )

            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

            return {
                'success': True,
                'transaction_hash': tx_hash.hex()
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

class QRCodeService:
    @staticmethod
    def generate_ticket_qr(ticket_data):
        """
        Generate QR code for a ticket
        ticket_data should contain: token_id, show_id, seat_number, user_wallet_address
        """
        # Create QR code data as JSON string
        qr_data = json.dumps({
            'token_id': ticket_data['token_id'],
            'show_id': ticket_data['show_id'],
            'seat_number': ticket_data['seat_number'],
            'user_wallet_address': ticket_data['user_wallet_address']
        })

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to bytes
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        qr_bytes = buffer.getvalue()
        
        # Convert to base64
        qr_base64 = base64.b64encode(qr_bytes).decode('utf-8')
        
        return {
            'success': True,
            'qr_code': qr_base64,
            'qr_data': qr_data
        }

    @staticmethod
    def verify_qr_code(qr_data):
        """
        Verify QR code data
        """
        try:
            # Parse QR code data
            ticket_data = json.loads(qr_data)
            
            # Validate required fields
            required_fields = ['token_id', 'show_id', 'seat_number', 'user_wallet_address']
            for field in required_fields:
                if field not in ticket_data:
                    return {
                        'success': False,
                        'error': f'Missing required field: {field}'
                    }
            
            return {
                'success': True,
                'ticket_data': ticket_data
            }
        except json.JSONDecodeError:
            return {
                'success': False,
                'error': 'Invalid QR code data format'
            } 