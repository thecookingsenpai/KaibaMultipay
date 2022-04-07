from __future__ import annotations
from bitcoinlib.wallets import Wallet
from kaibamultipay.modules import Module
from kaibamultipay.errors import *

import logging
logger = logging.getLogger("kaibamultipay")

class BitcoinModule(Module):
    """A bitcoin/litecoin module. 
    Wallet is managed through 
    [bitcoinlib](https://github.com/1200wd/bitcoinlib).

    A library allows to create wallets for different networks

    A new wallet can be created from 
    [command line](https://bitcoinlib.readthedocs.io/en/latest/
    source/_static/manuals.command-line-wallet.html)

    A library connects and submits to public APIs. 
    But it is possible and advised to setup a 
    bitcoin node [locally](https://bitcoinlib.readthedocs.io/
    en/latest/source/_static/manuals.setup-bitcoind-connection.html)
    """

    _wallet: Wallet
    _currency_name: str

    def __init__(self, wallet_name: str, currency_name: str):
        """
        :param wallet_name: Wallet name in bitcoinlib
        :param currency_name: A symbol of native currency(BTC, LTC, etc)
        """

        self._wallet = Wallet(wallet_name)
        self._currency_name = currency_name

    def send(self, currency: str, address: str, amount: int) -> str:
        """
        :param amount: Amount of sathoshi to send
        :param currency: A currency in which to send. 
        Same as in :py:meth:`BitcoinModule.__init__`
        :param address: Address of reciever
        :return: txid
        :raises: :py:class:`kaibamultipay.errors.NoSuchCurrencyError` 
        """

        if currency == self._currency_name:
            return self._send_native(address, amount)
        else:
            raise NoSuchCurrencyError(currency)

    def _send_native(self, address, amount):
        tx = self._wallet.send_to(address, amount, offline=False)
        logger.info(f"Bitcoin sent: {str(tx.txid)}")
        return tx.txid

    @staticmethod
    def from_config(config) -> BitcoinModule:
        """Create a BitcoinModule from config
        
        Config parameters:

        `native: str` - A `currency_name` as in :py:meth:`BitcoinModule.__init__`

        `wallet: str` - A wallet name in bitcoinlib

        Example:
        ```python
        {
            "native": "BTC",
            "wallet": "testnet_bitcoin"
        }
        ```
        """
        try:
            native = config.get("native", "BTC")
            wallet_name = config["wallet"]
        except KeyError as e:
            raise ConfigParseError(f"{e} is required in Bitcoin/Litecoin module config") from e

        result = BitcoinModule(wallet_name, native)
        return result
