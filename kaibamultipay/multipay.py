from audioop import add
from kaibamultipay.modules import *
import kaibamultipay.factory as factory
from kaibamultipay.errors import *

import logging
logger = logging.getLogger("kaibamultipay")

class Multipay:
    _pay: dict[str, Module]

    def __init__(self) -> None:
        self._pay = {}

    def register(self, chain: str, module: Module):
        self._pay[chain] = module

    def send(self, chain: str, currency: str, address: str, amount: int):
        logger.info(f"{chain} send {amount} {currency} to {address}")        

        if chain not in self._pay:
            raise NoSuchChainError(chain)

        try:
            return self._pay[chain].send(currency, address, amount)
        except Exception as e:
            raise SendError(chain, currency, address, amount) from e

    @staticmethod
    def from_config(config: dict):
        result = Multipay()

        for chain_name in config:
            chain_config = config[chain_name]

            try:
                type = chain_config["type"]
            except KeyError as e:
                raise ConfigParseError("\"type\" field is required in {chain_name} chain config") from e

            chain = factory.from_config(type, chain_config)
            result.register(chain_name, chain)

        return result


