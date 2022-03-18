from enum import Enum
from kaibamultipay.modules import *
from kaibamultipay.modules.solana import SolanaModule

class Types(Enum):
    ETHEREUM = {"from_config": EthereumModule.from_config}
    SOLANA = {"from_config": SolanaModule.from_config}

def from_config(type, config):
    return Types[type].value["from_config"](config)

