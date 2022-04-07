
from __future__ import annotations
from pathlib import Path
from kaibamultipay.errors import NoSuchCurrencyError, ConfigParseError

from kaibamultipay.modules import Module
from erdpy.accounts import Account
from erdpy.transactions import Transaction
from erdpy.proxy import ElrondProxy
from erdpy.proxy.http_facade import do_get
from erdpy.errors import ProxyRequestError


import logging
logger = logging.getLogger("kaibamultipay")


class ElrondModule(Module):
    """Elrond module to send currency"""

    _proxy: ElrondProxy
    _currency_name: str

    def __init__(self, endpoint: str, currency_name: str, pem_file: Path):
        """
        :param endpoint: API endpoint to connect to
        :param currency_name: A symbol of native currency(EGLD)
        :param pem_file: A path to pem file used to control address
        """

        pem_file = Path(pem_file)
        self._proxy = ElrondProxy(endpoint)
        self._account = Account(pem_file=str(pem_file))
        self._account.sync_nonce(self._proxy)
        self._currency_name = currency_name

        # Parse the network config by hand. 
        # Currently there is no min_gas_limit field in erdpy sdk
        url = f"{self._proxy.url}/network/config"
        response = do_get(url)
        data = response.get("config")
        self.min_gas_price = data.get("erd_min_gas_price", 0)
        self.min_gas_limit = data.get("erd_min_gas_limit", 0)
        self.chain_id = data.get("erd_chain_id", "?")
        self.min_tx_version = data.get("erd_min_transaction_version", 0)

    def _update_nonce(self):
        self._account.sync_nonce(self._proxy)
        logger.debug(f"Elrond updated nonce: {self._account.nonce}")

    def send(self, currency: str, address: str, amount: int) -> str:
        """Send `amount` of `currency` to an `address`
        
        :return: txid
        :raises: :py:class:`kaibamultipay.errors.NoSuchCurrencyError` 
        """

        try:
            if currency == self._currency_name:
                return self._send_native(address, amount)
            else:
                raise NoSuchCurrencyError(currency)
        except ProxyRequestError as e:
            message = e.args[0]
            if 'invalid transaction lowerNonceInTx: true' in message:
                self._update_nonce()
                return self.send(currency, address, amount)
            else:
                raise

    def _send_native(self, address, amount):
        transaction = Transaction()
        transaction.nonce = self._account.nonce
        transaction.sender = self._account.address.bech32()
        transaction.receiver = address
        transaction.value = str(amount)
        transaction.gasPrice = self.min_gas_price
        transaction.gasLimit = self.min_gas_limit
        transaction.chainID = self.chain_id
        transaction.version = self.min_tx_version
        transaction.sign(self._account)
        self._account.nonce += 1

        tx_hash = transaction.send(self._proxy)
        logger.info(f"Elrond sent: {str(tx_hash)}")
        return tx_hash

    @staticmethod
    def from_config(config) -> ElrondModule:
        """Create a ElrondModule from config
        
        Config parameters:

        `native: str` - A `currency_name` as in 
        :py:meth:`ElrondModule.__init__`

        `endpoint: str` - An API endpoint

        `private_key: str` - A path to a .pem file

        :raises: :py:class:`kaibamultipay.errors.ConfigParseError` 
        if required parameters is not found
        """

        try:
            endpoint = config["endpoint"]
            native = config.get("native", "EGLD")
            private_key = config["private_key"]
        except KeyError as e:
            raise ConfigParseError(f"{e} is required in ELROND module config") from e

        result = ElrondModule(
            endpoint, native, Path(private_key))

        return result
