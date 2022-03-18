import web3
from web3.middleware import geth_poa_middleware
from kaibamultipay.modules import Module
from kaibamultipay.abi import EIP20_ABI

import logging
logger = logging.getLogger("kaibamultipay")


class EthereumModule(Module):
    _w3: web3.Web3
    _erc20: dict
    _currency_name: str
    _key: str

    def __init__(self, endpoint, currency_name, private_key) -> None:
        self._w3 = web3.Web3(web3.HTTPProvider(endpoint))
        self._w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self._key = private_key
        self._currency_name = currency_name
        self._erc20 = {}
        self._chain_id = self._w3.eth.chain_id
        self._last_nonce = self._w3.eth.get_transaction_count(
            web3.Account.from_key(self._key).address, 'latest')

    def send(self, currency: str, address: str, amount: int):
        logger.info(f"{self._currency_name} send {currency}")
        if currency == self._currency_name:
            self._send_native(address, amount)
        else:
            self._send_erc20(self._erc20[currency], address, amount)

    def _send_native(self, address, amount):
        nonce = self._w3.eth.get_transaction_count(
            web3.Account.from_key(self._key).address, 'latest')

        gas_price = self._w3.eth.gas_price
        transaction = {
            'to': address,
            'value': amount,
            'gas': 21000,
            'gasPrice': gas_price,
            'nonce': self._last_nonce,
            'chainId': self._chain_id,
        }

        signed = self._w3.eth.account.sign_transaction(transaction, self._key)

        self._last_nonce += 1
        self._w3.eth.send_raw_transaction(signed.rawTransaction)
        logger.debug("Sent")

    def _send_erc20(self, contract_addr, address, amount):
        contract = self._w3.eth.contract(contract_addr, abi=EIP20_ABI)
        nonce = self._w3.eth.get_transaction_count(
            web3.Account.from_key(self._key).address, 'latest')

        gas_price = self._w3.eth.gas_price
        transaction = contract.functions.transfer(address, amount).buildTransaction({
            'chainId': self._chain_id,
            'gas': 700000,
            'gasPrice': gas_price,
            'nonce': nonce,
        })

        signed = self._w3.eth.account.sign_transaction(transaction, self._key)

        self._last_nonce += 1
        self._w3.eth.send_raw_transaction(signed.rawTransaction)

        logger.debug("ERC20 Sent")

    def add_erc20(self, name, address):
        self._erc20[name] = address

    @staticmethod
    def from_config(config):
        result = EthereumModule(
            config["endpoint"], config["native"], config["private_key"])
        if "erc20" in config:
            for token_name, address in config["erc20"].items():
                result.add_erc20(token_name, address)

        return result
