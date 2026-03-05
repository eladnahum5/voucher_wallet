"""
Voucher class for Voucher Wallet integration.
Currently not in use, but can be used in the future if needed.
"""

from const import DOMAIN


class Voucher:
    """Class representing a voucher in the Voucher Wallet integration."""

    def __init__(self, code: int, value: float, redeemed: bool=False):
        """Initialize a Voucher instance."""
        self.code = code
        self.value = value
        self.redeemed = redeemed

        hass.data[DOMAIN]["db"].add_voucher(code, value, redeemed) # type: ignore

    def __repr__(self):
        """Return a string representation of the Voucher."""
        return f"Voucher(code={self.code}, value={self.value}, redeemed={self.redeemed})"