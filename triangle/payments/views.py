from web3 import Web3
from web3.middleware import geth_poa_middleware

from bases.views import *
from .models import Transaction
from .serializers import *

from django.conf import settings

__all__ = ['OutputView', 'InputView']


def get_web3_remote_provider():
    web3 = Web3(Web3.HTTPProvider(settings.BLOCKCHAIN_RPC_URL))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    web3.eth.default_account = settings.BANK_ADDRESS

    return web3


def get_token_contract(web3, abi):
    addr = web3.toChecksumAddress(settings.BLOCKCHAIN_TOKEN_ADDRESS)
    return web3.eth.contract(address=addr, abi=abi)


class InputView(BaseView, CreateAPIView):
    serializer_class = InputSerializer

    def check_post_perms(self, request):
        self.check_anonymous(request)
        if Transaction.objects.filter(hash=request.data['hash']).exists():
            raise APIException('This transaction already registered.')

    def perform_create(self, serializer):
        hash_str = self.request.data['hash'][2:]

        web3 = get_web3_remote_provider()
        transaction = web3.eth.get_transaction(bytes.fromhex(hash_str))

        abi = [
            {
                "constant": False,
                "inputs": [
                    {"name": "to", "type": "address"},
                    {"name": "value", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function",
            }
        ]
        contract = get_token_contract(web3, abi)
        transaction_info = contract.decode_function_input(transaction.input)[1]

        if transaction_info["to"] != settings.BANK_ADDRESS:
            raise APIException('Payment recipient is not service wallet.')

        user = self.request.user
        user.coins += int(transaction_info["value"])
        user.save()

        serializer.save(
            user=user,
            type=Transaction.TYPES.INPUT,
            wallet_amount=int(transaction_info["value"]),
            coins_amount=int(transaction_info["value"]),
            blockchain_address=transaction["from"]
        )


class OutputView(BaseView, CreateAPIView):
    serializer_class = OutputSerializer

    def check_post_perms(self, request):
        self.check_anonymous(request)
        if request.data['coins_amount'] < 10**18:
            raise APIException("Minimal withdrawal amount is 10^18 coins.")
        if request.data['coins_amount'] < request.user.coins:
            raise APIException('Not enough coins.')

    def perform_create(self, serializer):
        web3 = get_web3_remote_provider()
        abi = [
            {
                "constant": False,
                "inputs": [
                    {"name": "_to", "type": "address"},
                    {"name": "_value", "type": "uint256"},
                ],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function",
            }
        ]
        contract = get_token_contract(web3, abi)
        withdrawal_amount = int(self.request.data['coins_amount'] * 0.9)

        transfer = contract.functions.transfer(
            self.request.data['blockchain_address'], withdrawal_amount
        ).buildTransaction(
            {
                "chainId": 56,
                "gas": settings.OUTPUT_GAS_COUNT,
                "gasPrice": web3.eth.gasPrice,
                "nonce": web3.eth.getTransactionCount(settings.BANK_ADDRESS),
            }
        )
        account = web3.eth.account.privateKeyToAccount(settings.BANK_PRIVATE_KEY)
        signed_transfer = account.signTransaction(transfer)
        sent_transfer = web3.eth.sendRawTransaction(signed_transfer.rawTransaction)

        user = self.request.user
        user.coins -= self.request.data['coins_amount']
        user.save()

        serializer.save(
            user=user,
            type=Transaction.TYPES.OUTPUT,
            wallet_amount=withdrawal_amount,
            hash=sent_transfer.hex()
        )
