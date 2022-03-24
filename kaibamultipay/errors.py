
class MultipayError(Exception):
    pass

class SendError(MultipayError):
    pass

class NoSuchCurrencyError(MultipayError):
    pass

class NoSuchChainError(MultipayError):
    pass 

class ConfigParseError(MultipayError):
    pass
