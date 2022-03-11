import datetime
import time

from constants import DEBUG
import utils

CommonConstants, BuyConstants, SellConstants = utils.get_constants()


class BuyController:
    def __init__(self, web3, router):
        self.web3 = web3
        self.router = router

    def buy(self, token_address):
        transaction = self.__init_transaction(token_address)
        transaction = self.__finalize_transaction(transaction)

        transaction_hash = utils.sign_and_send_transaction(transaction)
        hash_as_hex = self.web3.toHex(transaction_hash)

        utils.wait_for_complete(self.web3, hash_as_hex)

        return hash_as_hex

    def __init_transaction(self, token_address):
        return self.router.functions.swapExactETHForTokens(
            BuyConstants.TRANSACTION_ARG_1,
            [
                self.web3.toChecksumAddress(CommonConstants.WBNB),
                self.web3.toChecksumAddress(token_address),
            ],
            CommonConstants.MY_PURSE_ADDRESS,
            BuyConstants.DEADLINE
        )

    def __finalize_transaction(self, transaction):
        return transaction.buildTransaction({
            'value': BuyConstants.BNB_TO_SPEND,
            'from': self.web3.toChecksumAddress(CommonConstants.MY_PURSE_ADDRESS),
            'gas': BuyConstants.GAS,
            'gasPrice': BuyConstants.GAS_PRICE,
            'nonce': self.web3.eth.get_transaction_count(CommonConstants.MY_PURSE_ADDRESS)
        })


class SellController:
    def __init__(self, web3, router):
        self.web3 = web3
        self.router = router

    def sell(self, token_address):
        self.__setup(token_address)

        self.__aprove()
        if DEBUG:
            self.__wait_for_10s_sleep(datetime.timedelta(seconds=0))
        else:
            time_in_api_calls = self.__wait_for_price()
            self.__wait_for_10s_sleep(time_in_api_calls)

        transaction_hash = self.__make_transaction(self.balance, token_address)

        return self.web3.toHex(transaction_hash)

    def __setup(self, token_address):
        self.sell_contract = self.web3.eth.contract(
            address=self.web3.toChecksumAddress(token_address),
            abi=SellConstants.SELL_ABI
        )
        self.balance = self.sell_contract.functions.balanceOf(
            CommonConstants.MY_PURSE_ADDRESS
        ).call()

    def __aprove(self):
        approve = self.sell_contract.functions.approve(
            self.router.address, self.balance
        ).buildTransaction({
            'from': CommonConstants.MY_PURSE_ADDRESS,
            'gas': SellConstants.GAS,
            'gasPrice': SellConstants.GAS_PRICE,
            'nonce': self.web3.eth.get_transaction_count(CommonConstants.MY_PURSE_ADDRESS)
        })
        transaction_hash = utils.sign_and_send_transaction(approve)
        hash_as_hex = self.web3.toHex(transaction_hash)
        utils.wait_for_complete(self.web3, hash_as_hex)

    def __wait_for_price(self):
        start = datetime.datetime.now()

        token_price = utils.check_price(address=self.sell_contract.address)
        while token_price < SellConstants.USD_MIN_PRICE:
            time.sleep(2)
            token_price = utils.check_price(address=self.sell_contract.address)
        end = datetime.datetime.now()

        time_in_api_calls = end - start
        return time_in_api_calls

    def __wait_for_10s_sleep(self, spended_time):
        time_to_sleep = 0 if spended_time.seconds >= 10 else 10 - spended_time.seconds
        time.sleep(time_to_sleep)

    def __make_transaction(self, sell_amount, token_address):
        transaction = self.__init_transaction(sell_amount, token_address)
        transaction = self.__finalize_transaction(
            transaction,
            self.web3.eth.get_transaction_count(CommonConstants.MY_PURSE_ADDRESS)
        )
        transaction_hash = utils.sign_and_send_transaction(transaction)
        hash_as_hex = self.web3.toHex(transaction_hash)
        utils.wait_for_complete(self.web3, hash_as_hex)
        return transaction_hash

    def __init_transaction(self, sell_amount, token_address):
        return self.router.functions.swapExactTokensForETH(
            sell_amount,
            SellConstants.TOKEN_TO_SELL_OUT_MIN,
            [
                self.web3.toChecksumAddress(token_address),
                self.web3.toChecksumAddress(CommonConstants.WBNB),
            ],
            self.web3.toChecksumAddress(CommonConstants.MY_PURSE_ADDRESS),
            SellConstants.DEADLINE
        )

    def __finalize_transaction(self, transaction, nonce):
        return transaction.buildTransaction({
            'from': self.web3.toChecksumAddress(CommonConstants.MY_PURSE_ADDRESS),
            'gas': SellConstants.GAS,
            'gasPrice': SellConstants.GAS_PRICE,
            'nonce': nonce
        })
