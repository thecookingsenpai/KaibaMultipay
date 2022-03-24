import pytest
import kaibamultipay

def test_no_such_chain():
    multipay = kaibamultipay.Multipay()
    with pytest.raises(kaibamultipay.NoSuchChainError):
        multipay.send("ETHEREUM", "ETH", "0xD92E713d051C37EbB2561803a3b5FBAbc4962431", 1000000000)

def test_from_config_parse_error():
    config = {
        "Chain": {
            "type": "NON_EXISTENT_TYPE",
        },
    }

    with pytest.raises(kaibamultipay.ConfigParseError):
        kaibamultipay.Multipay.from_config(config)
