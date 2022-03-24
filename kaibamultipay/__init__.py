import logging
logging.getLogger('kaibamultipay').addHandler(logging.NullHandler())

from kaibamultipay.modules import *
from kaibamultipay.multipay import *
