import pytest
import kaibamultipay

def test_from_config_parse_error():
    config = {}

    with pytest.raises(kaibamultipay.ConfigParseError):
        kaibamultipay.EthereumModule.from_config(config)
