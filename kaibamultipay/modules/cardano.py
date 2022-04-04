from kaibamultipay.modules.base import Module
from kaibamultipay.errors import *
import cardano.numbers
from cardano.wallet import Wallet
from cardano.backends.walletrest import WalletREST

import logging
logger = logging.getLogger("kaibamultipay")

class CardanoModule(Module):
    _wallet: Wallet
    _currency_name: str

    def __init__(self, currency_name, wallet_id: str, host='localhost', port=8090, passphrase=None) -> None:
        self._passphrase = passphrase
        self._wallet = Wallet(wallet_id, backend=WalletREST(port=port, host=host))               
        self._currency_name = currency_name


    def send(self, currency: str, address: str, amount: int):
        if currency == self._currency_name:
            return self._send_native(address, amount)
        else:
            raise NoSuchCurrencyError(currency)

    def _send_native(self, address, amount):
        logger.debug(f"Cardano wallet sync proggress: {self._wallet.sync_progress()}")
        logger.debug(f"Cardano wallet balance: {self._wallet.balance()}")

        tx = self._wallet.transfer(address, cardano.numbers.from_lovelaces(
            amount), passphrase=self._passphrase)
        logger.info(f"Cardano sent: {str(tx.txid)}")
        return tx.txid

    @staticmethod
    def from_config(config):
        try:
            host = config.get("host", "localhost")
            port = config.get("port", 8090)
            native = config.get("native", "ADA")
            passphrase = config.get("passphrase")
            wallet_id = config["wallet_id"]
        except KeyError as e:
            raise ConfigParseError(f"{e} is required in Cardano module config") from e

        result = CardanoModule(native, wallet_id, host, port, passphrase=passphrase)

        return result
