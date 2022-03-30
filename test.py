import json
import logging
import kaibamultipay
logging.getLogger("kaibamultipay").addHandler(logging.StreamHandler())
logging.getLogger("kaibamultipay").setLevel(logging.DEBUG)

multipay = kaibamultipay.Multipay.from_config(json.load(open("example_config.json")))

multipay.send("ETHEREUM", "USDT", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 100000)
multipay.send("ETHEREUM", "ETH", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 1000000000000000)
multipay.send("FANTOM", "FTM", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)
multipay.send("BSC", "BNB", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)

multipay.send("ELROND", "EGLD", "erd139m36k859j8dm4zsaulqz8s6xe64t7z2ynrm6n7dwe8kfsg72e4qxywwsx", 10000000000000000)  # 0.01 EGLD

multipay.send("SOLANA", "SOL", "5cdXDJuxhjdiR1QF5iWKCmx6ziLw4ZqYNMqwRHGuosQ", 10000000) #0.01 sol

multipay.send("CARDANO", "ADA", "addr_test1qqe6dqhlvyqjpjn89jdny5eqa8ansl8638gqyxjf8g6p65evha6fpdde4jjj6tgx8p423hx9pguw2czy5qe7ed7pac7stqgd5g", 100000) # 1 ADA
