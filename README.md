# KaibaMultipay
Python module that connects to the wallets or accounts on multiple chains and has a generic interface to send a currency to an address on a specified chain

## Installing
Project uses [poetry](https://python-poetry.org/) to manage dependencies and packaging

After downloading the repository use 
```
poetry install
```
to install the dependencies. And then run

```
poetry build
```
This will create dist directory with package files. After that the .whl file can be installed with `pip install path/to/whl`

## Using

Example registering modules programmaticaly

``` python
from kaibamultipay import Multipay, EthereumModule

pay = Multipay()
ftm = EthereumModule("https://rpc.testnet.fantom.network/", "FTM", "904ebe905db0bb2afadbdd0dae4eedf51d7206152d776a88ac3df1eddc945420")
bsc = EthereumModule("https://data-seed-prebsc-1-s1.binance.org:8545/", "BNB", "904ebe905db0bb2afadbdd0dae4eedf51d7206152d776a88ac3df1eddc945420")

pay.register("FANTOM", ftm)
pay.register("BSC", bsc)

pay.send("FANTOM", "FTM", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)
pay.send("BSC", "BNB", "0x74dF2671D4c080289E1826b878De62d8dB9316e0", 10000000000000000)
```

There is an [example](test.py) of loading `Multipay` from [example](example_config.json) config.

Supported config module types can be found [here](kaibamultipay/factory.py)

Structure of each module config is explained in documentation for `from_config` function
## Documentation
[pdoc](https://pdoc.dev/) can be used.

After installing dependencies with `poetry install` you can generate documentation
```
poetry run pdoc kaibamultipay
```
This will generate the documentation, start the http server and open a tab in browser
## Logging
Module uses logging module and adds a logger named `kaibamultipay`

Example enabling printing to console
``` python
import logging
import kaibamultipay
logging.getLogger("kaibamultipay").addHandler(logging.StreamHandler())
logging.getLogger("kaibamultipay").setLevel(logging.DEBUG)
```
