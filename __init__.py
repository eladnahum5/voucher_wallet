from __future__ import annotations


from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .sqlite_helper import VoucherWalletDatabase
from .views import AddVoucherView, RemoveVoucherView

import sqlite3


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Voucher Wallet integration."""

    db = VoucherWalletDatabase(hass)  # Initialize the database
    hass.data[DOMAIN] = {"db": db}  # Store the database instance in hass.data for later use

    hass.http.register_view(AddVoucherView)
    hass.http.register_view(RemoveVoucherView)

    # Return boolean to indicate that initialization was successfully.
    return True