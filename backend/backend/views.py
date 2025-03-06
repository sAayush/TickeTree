from django.http import JsonResponse
from .blockchain import Blockchain
import json

blockchain = Blockchain()

def create_transaction(request):
    data = json.loads(request.body)
    required_fields = ['sender', 'recipient', 'amount']

    if not all(field in data for field in required_fields):
        return JsonResponse({'message': 'Missing values'}, status=400)

    index = blockchain.new_transaction(data['sender'], data['recipient'], data['amount'])
    return JsonResponse({'message': f'Transaction will be added to Block {index}'}, status=201)

def mine_block(request):
    last_block = blockchain.last_block
    proof = 100  # This should be replaced with a proof of work algorithm
    block = blockchain.new_block(proof)

    response = {
        'message': 'New block mined',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
    }
    return JsonResponse(response, status=200) 