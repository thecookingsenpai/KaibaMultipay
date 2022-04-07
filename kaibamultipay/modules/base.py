
class Module:
    """A base class for modules"""

    def send(self, currency: str, address: str, amount: int) -> str:
        """Send an `amount` of `currency` to an `address`"""
