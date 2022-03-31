from enum import Enum
from kaibamultipay.errors import ConfigParseError
from kaibamultipay.modules import *

class Types(Enum):
    ETHEREUM = {"from_config": EthereumModule.from_config}
    ELROND = {"from_config": ElrondModule.from_config}
    SOLANA = {"from_config": SolanaModule.from_config}

def from_config(type, config):
    try:
        module_type = Types[type]
    except KeyError as e:
        raise ConfigParseError(f"No such module type: {str(e)}") from e

    return module_type.value["from_config"](config)

