import web3
from web3.middleware import geth_poa_middleware
from kaibamultipay.modules import Module
from kaibamultipay.errors import *
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
        self._update_nonce()

    # amount units are wei or token units depending on currency
    def send(self, currency: str, address: str, amount: int):
        try:
            if currency == self._currency_name:
                return self._send_native(address, amount)
            else:
                try:
                    contract_address = self._erc20[currency]
                except KeyError as e:
                    raise NoSuchCurrencyError(currency)

                return self._send_erc20(contract_address, address, amount)
        except ValueError as e:
            message = e.args[0]["message"] 
            if message == 'nonce too low' or message == 'replacement transaction underpriced':
                self._update_nonce()
                return self.send(currency, address, amount)
            else:
                raise
            

    def _update_nonce(self):
        self._last_nonce = self._w3.eth.get_transaction_count(
            web3.Account.from_key(self._key).address, 'latest')
        logger.debug(f"Ethereum updated nonce: {self._last_nonce}")

    # amount is in wei units
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
        tx_id = self._w3.eth.send_raw_transaction(signed.rawTransaction)
        logger.debug(f"Ethereum module sent {self._w3.toHex(tx_id)}")
        return self._w3.toHex(tx_id)

    # amount is in token units
    def _send_erc20(self, contract_addr, address, amount):
        contract = self._w3.eth.contract(contract_addr, abi=EIP20_ABI)
        nonce = self._w3.eth.get_transaction_count(
            web3.Account.from_key(self._key).address, 'latest')

        gas_price = self._w3.eth.gas_price
        transaction = contract.functions.transfer(address, amount).buildTransaction({
            'chainId': self._chain_id,
            'gas': 700000,
            'gasPrice': gas_price,
            'nonce': self._last_nonce,
        })

        signed = self._w3.eth.account.sign_transaction(transaction, self._key)

        self._last_nonce += 1
        tx_id = self._w3.eth.send_raw_transaction(signed.rawTransaction)

        logger.debug(f"ERC20 Sent: {self._w3.toHex(tx_id)}")
        return self._w3.toHex(tx_id)

    def add_erc20(self, name, address):
        self._erc20[name] = address

    @staticmethod
    def from_config(config):
        try:
            endpoint = config["endpoint"]
            native = config["native"]
            private_key = config["private_key"]
        except KeyError as e:
            raise ConfigParseError(f"{e} is required in Ethereum module config") from e

        result = EthereumModule(endpoint, native, private_key)

        if "erc20" in config:
            for token_name, address in config["erc20"].items():
                result.add_erc20(token_name, address)

        return result
