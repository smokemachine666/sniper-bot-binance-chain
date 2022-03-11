import time

from web3 import Web3


class CommonConstants:
    BSC = 'https://data-seed-prebsc-1-s1.binance.org:8545/'
    PROVIDER = Web3(Web3.HTTPProvider(BSC))

    WBNB = '0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd'

    MY_PURSE_ADDRESS = '0xAE89a2895399512d5898c3c7D3b80a226fD8Bf22'
    MY_PRIVATE_KEY = '5883673fd9933cd2f91cec5977ef3b52e9cf8d6dbe58b1c7250982cc80612bbd'

    # OLD
    # PANCAKE_ROUTER_ADDRESS = '0xD99D1c33F9fC3444f8101754aBC46c52416550D1'

    PANCAKE_ROUTER_ADDRESS = '0x9Ac64Cc6e4415144C455BD8E4837Fea55603e5c3'
    PANCAKE_ROUTER_ABI = open('./data/router_testnet_abi2.json').read()

    TOKEN_TO_WORK_WITH = '0x78867bbeef44f2326bf8ddd1941a4439382ef2a7'


class BuyConstants:
    TRANSACTION_ARG_1 = 0

    BNB_TO_SPEND = Web3.toWei(0.05, 'ether')

    DEADLINE = (int(time.time()) + 10000)

    GAS = Web3.toWei('200', 'kwei')
    GAS_PRICE = Web3.toWei('10', 'gwei')


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

    WEI_AMOUNT = 'ether'

    USD_MIN_PRICE = 0

    TOKEN_TO_SELL_OUT_MIN = 0

    DEADLINE = (int(time.time()) + 1000000)

    GAS = Web3.toWei('200', 'kwei')
    GAS_PRICE = Web3.toWei('10', 'gwei')
