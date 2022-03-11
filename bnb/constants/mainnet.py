import time

from web3 import Web3


class CommonConstants:
    BSC = 'https://speedy-nodes-nyc.moralis.io/e869f69a4e43b1d89f5e153d/bsc/mainnet'
    PROVIDER = Web3(Web3.HTTPProvider(BSC))

    WBNB = '0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c'

    MY_PURSE_ADDRESS = ''
    MY_PRIVATE_KEY = ''

    PANCAKE_ROUTER_ADDRESS = '0x10ED43C718714eb63d5aA57B78B54704E256024E'
    PANCAKE_ROUTER_ABI = open('./data/pancake_router_abi.json').read()

    TOKEN_TO_WORK_WITH = '0x9755ac467BEE2E7558B89988Df3dE4cA4f16b123'


class BuyConstants:
    TRANSACTION_ARG_1 = 0 

    BNB_TO_SPEND = Web3.toWei(0.0002, 'ether')
    DEADLINE = (int(time.time()) + 10000)

    GAS = Web3.toWei('200', 'kwei')
    GAS_PRICE = Web3.toWei('6', 'gwei')


class SellConstants:
    '''
    https://web3py.readthedocs.io/en/stable/examples.html?highlight=mwei#converting-currency-denominations

    mwei = 6 decimals
    gwei = 9 decimals
    microether = 12 decimals
    milliether = 15 decimals
    ether = 18 decimals
    '''
    SELL_ABI = open('./data/sell_abi.json').read()

    WEI_AMOUNT = 'mwei'

    USD_MIN_PRICE = 5.1

    TOKEN_TO_SELL_OUT_MIN = 0

    DEADLINE = (int(time.time()) + 1000000)

    GAS = Web3.toWei('200', 'kwei')
    GAS_PRICE = Web3.toWei('5', 'gwei')
