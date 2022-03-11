import traceback

from web3 import Web3

try:
    from constants import DEBUG
    if not DEBUG:
        from constants.mainnet import CommonConstants 
    else:
        from constants.testnet import CommonConstants 
except Exception:
    from constants.testnet import CommonConstants

import controllers

web3 = Web3(Web3.HTTPProvider(CommonConstants.BSC))


def main(bcontroller: controllers.BuyController, scontroller: controllers.SellController):
    print('buying...')
    buy_hash = bcontroller.buy(CommonConstants.TOKEN_TO_WORK_WITH)
    print(f'bought. purchase hash: {buy_hash}')
    print('now selling...')
    sell_hash = scontroller.sell(CommonConstants.TOKEN_TO_WORK_WITH)
    print(f'sold. sell hash: {sell_hash}')

if __name__ == '__main__':
    pancake_router = web3.eth.contract(
        address=CommonConstants.PANCAKE_ROUTER_ADDRESS,
        abi=CommonConstants.PANCAKE_ROUTER_ABI
    )

    buy_controller = controllers.BuyController(web3=web3, router=pancake_router)
    sell_controller = controllers.SellController(web3=web3, router=pancake_router)

    try:
        main(bcontroller=buy_controller, scontroller=sell_controller)
    except Exception:
        print(traceback.format_exc())
    input('Enter to exit')
