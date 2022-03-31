from bitcoinlib.wallets import Wallet
from kaibamultipay.modules import Module
from kaibamultipay.errors import *

import logging
logger = logging.getLogger("kaibamultipay")

class BitcoinModule(Module):
    _wallet: Wallet
    _currency_name: str

    def __init__(self, wallet_name, currency_name) -> None:
        self._wallet = Wallet(wallet_name)
        self._currency_name = currency_name

    def send(self, currency: str, address: str, amount: int):
        if currency == self._currency_name:
            return self._send_native(address, amount)
        else:
            raise NoSuchCurrencyError(currency)

    def _send_native(self, address, amount):
        tx = self._wallet.send_to(address, amount, offline=False)
        logger.info(f"Bitcoin sent: {str(tx.txid)}")
        return tx.txid

    @staticmethod
    def from_config(config):
        try:
            native = config.get("native", "BTC")
            wallet_name = config["wallet"]
        except KeyError as e:
            raise ConfigParseError(f"{e} is required in Bitcoin module config") from e

        result = BitcoinModule(wallet_name, native)
        return result
