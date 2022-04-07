
class MultipayError(Exception):
    '''A base class for other exceptions'''

class SendError(MultipayError):
    '''Thrown if an error occurs in multipay send function'''

class NoSuchCurrencyError(MultipayError):
    '''Thrown if there is no such currency in module'''

class NoSuchChainError(MultipayError):
    '''Thrown if there is no such chain in multipay'''
    pass 

class ConfigParseError(MultipayError):
    '''Thrown in the case module config is wrong(missing parameters, etc)'''

class TimeoutError(MultipayError):
    '''Thrown if timeout occurs while waiting for  
    transaction confirm(currently only in cardano)'''
