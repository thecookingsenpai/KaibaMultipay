from kaibamultipay.modules import *
import kaibamultipay.factory as factory

import logging
logger = logging.getLogger("kaibamultipay")

class Multiplay:
    _pay: dict[str, Module]

    def __init__(self) -> None:
        self._pay = {}

    def register(self, chain: str, module: Module):
        self._pay[chain] = module

    def send(self, chain: str, currency: str, address: str, amount: int):
        logger.info(f"Send {chain} {currency}")
        self._pay[chain].send(currency, address, amount)

    @staticmethod
    def from_config(config: dict):
        result = Multiplay()

        for chain_name in config:
            chain_config = config[chain_name]
            chain = factory.from_config(chain_config["type"], chain_config)
            result.register(chain_name, chain)

        return result


