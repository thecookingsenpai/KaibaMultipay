from __future__ import annotations
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
    """Elrond module to send currency"""

    _client: Client
    _currency_name: str
    _keypair: Keypair

    def __init__(self, endpoint: str, currency_name: str, private_key: bytes):
        """
        :param endpoint: API endpoint to connect to
        :param currency_name: A symbol of native currency(SOL)
        :param private_key: A bytes array
        """

        self._client = Client(endpoint)
        self._keypair = Keypair.from_secret_key(private_key)
        self._currency_name = currency_name

    def send(self, currency: str, address: str, amount: int) -> str:
        """Send `amount` of `currency` to an `address`
        
        `amount` units for native currency is in lamports

        :return: txid
        :raises: :py:class:`kaibamultipay.errors.NoSuchCurrencyError` 
        """

        if currency == self._currency_name:
            return self._send_native(address, amount)
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
        logger.info(f"Solana sent: {result['result']}")
        return result["result"]

    @staticmethod
    def from_config(config) -> SolanaModule:
        """Create a SolanaModule from config
        
        Config parameters:

        `native: str` - A `currency_name` as in 
        :py:meth:`SolanaModule.__init__`

        `endpoint: str` - An API endpoint

        `private_key: str` - A bytes array that represents a private key

        :raises: :py:class:`kaibamultipay.errors.ConfigParseError` 
        if required parameters is not found
        """

        try:
            endpoint = config["endpoint"]
            native = config.get("native", "SOL")
            private_key = config["private_key"]
        except KeyError as e:
            raise ConfigParseError(f"{e} is required in Solana module config") from e

        result = SolanaModule(
            endpoint, native, bytes(private_key))

        return result
