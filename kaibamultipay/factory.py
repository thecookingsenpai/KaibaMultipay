from enum import Enum
from kaibamultipay.modules import *

class Types(Enum):
    ETHEREUM = {"from_config": EthereumModule.from_config}
    ELROND = {"from_config": ElrondModule.from_config}

def from_config(type, config):
    return Types[type].value["from_config"](config)

