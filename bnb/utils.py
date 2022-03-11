import decimal

import requests
from web3.exceptions import TransactionNotFound

def get_constants():
    try:
        from constants import DEBUG
        if not DEBUG:
            from constants.mainnet import BuyConstants, CommonConstants, SellConstants
        else:
            from constants.testnet import BuyConstants, CommonConstants, SellConstants
    except Exception:
        from constants.testnet import BuyConstants, CommonConstants, SellConstants
    return CommonConstants, BuyConstants, SellConstants

CommonConstants, BuyConstants, SellConstants = get_constants()


def check_price(address):
    url = f'https://api.trading-tigers.com/PancakeSwap/tokenprice/{address}'
    try:
        resp = requests.get(url)
    except Exception:
        return 0
    price = resp.json()['USDprice']
    return decimal.Decimal(price)


def sign_transaction(transaction):
    return CommonConstants.PROVIDER.eth.account.signTransaction(
        transaction, CommonConstants.MY_PRIVATE_KEY
    )


def sign_and_send_transaction(transaction):
    signed_transaction = sign_transaction(transaction)
    transaction_hash = CommonConstants.PROVIDER.eth.send_raw_transaction(
        signed_transaction.rawTransaction
    )
    return transaction_hash


def wait_for_complete(web3, hash_as_hex):
    try:
        web3.eth.get_transaction_receipt(hash_as_hex)
    except TransactionNotFound:
        wait_for_complete(web3, hash_as_hex)
