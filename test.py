import json
import logging
import kaibamultipay
logging.getLogger("kaibamultipay").addHandler(logging.StreamHandler())
logging.getLogger("kaibamultipay").setLevel(logging.DEBUG)

multipay = kaibamultipay.Multiplay.from_config(json.load(open("example_config.json")))

multipay.send("ETHEREUM", "USDT", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 100000)
multipay.send("ETHEREUM", "ETH", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 1000000000000000)
multipay.send("FANTOM", "FTM", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)
multipay.send("BSC", "BNB", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)

multipay.send("SOLANA", "SOL", "5cdXDJuxhjdiR1QF5iWKCmx6ziLw4ZqYNMqwRHGuosQ", 10000000) #0.01 sol
