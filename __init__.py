from __future__ import annotations


from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .sqlite_helper import VoucherWalletDatabase

import sqlite3


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup our skeleton component."""
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.async_set('voucher_wallet.total_value', 0)

    db = VoucherWalletDatabase(hass)  # Initialize the database
    hass.data[DOMAIN] = {"db": db}  # Store the database instance in hass.data for later use

    # Return boolean to indicate that initialization was successfully.
    return True