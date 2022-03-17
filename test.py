import json
import logging
import kaibamultipay
import web3

from kaibamultipay.modules.ethereum import EthereumModule
logging.getLogger("kaibamultipay").addHandler(logging.StreamHandler())
logging.getLogger("kaibamultipay").setLevel(logging.DEBUG)

multipay = kaibamultipay.Multiplay.from_config(json.load(open("example_config.json")))

multipay.send("ETHEREUM", "USDT", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 100000)
multipay.send("ETHEREUM", "ETH", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 1000000000000000)
multipay.send("FANTOM", "FTM", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)
multipay.send("BSC", "BNB", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)
