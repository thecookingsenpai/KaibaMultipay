from kaibamultipay.modules import Module
from kaibamultipay.errors import NoSuchCurrencyError, ConfigParseError
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.system_program import transfer, TransferParams
from solana.publickey import PublicKey
from solana.keypair import Keypair

import logging
logger = logging.getLogger("kaibamultipay")


class SolanaModule(Module):
    _client: Client
    _currency_name: str
    _keypair: Keypair

    def __init__(self, endpoint, currency_name, private_key: bytes) -> None:
        self._client = Client(endpoint)
        self._keypair = Keypair.from_secret_key(private_key)
        self._currency_name = currency_name

    def send(self, currency: str, address: str, amount: int):
        logger.info(f"{self._currency_name} send {currency}")
        if currency == self._currency_name:
            self._send_native(address, amount)
        else:
            raise NoSuchCurrencyError(currency)

    def _send_native(self, address, amount):
        receiver = PublicKey(address)

        instruction = transfer(
            TransferParams(from_pubkey=self._keypair.public_key,
                           to_pubkey=receiver, lamports=amount)
        )

        transaction = Transaction()
        transaction.add(instruction)

        result = self._client.send_transaction(transaction, self._keypair)
        logger.info("Solana sent, response: ", result)

    @staticmethod
    def from_config(config):
        try:
            endpoint = config["endpoint"]
            native = config.get("native", "SOL")
            private_key = config["private_key"]
        except KeyError as e:
            raise ConfigParseError(f"{e} is required in Solana module config") from e

        result = SolanaModule(
            endpoint, native, bytes(private_key))

        return result
