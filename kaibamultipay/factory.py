from enum import Enum
from kaibamultipay.errors import ConfigParseError
from kaibamultipay.modules import *


class Types(Enum):
    '''Enumeration of supported modules.'''
    ETHEREUM = {"from_config": EthereumModule.from_config}
    ELROND = {"from_config": ElrondModule.from_config}
    SOLANA = {"from_config": SolanaModule.from_config}
    CARDANO = {"from_config": CardanoModule.from_config}
    BITCOIN = {"from_config": BitcoinModule.from_config}


def from_config(type: str, config: dict) -> Module:
    """Load a ``type`` module from ``config``
    
    :param type: The the type of a module as in :py:class:`Types`
    ("ETHEREUM" for example)
    :param config: The config of the module
    :return: Module loaded from ``config``
    :raises: :py:class:`kaibamultipay.errors.ConfigParseError` 
    if there is no such module type
    """

    try:
        module_type = Types[type]
    except KeyError as e:
        raise ConfigParseError(f"No such module type: {str(e)}") from e

    return module_type.value["from_config"](config)
