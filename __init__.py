from __future__ import annotations


from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .sqlite_helper import VoucherWalletDatabase
from .views import AddVoucherView, RemoveVoucherView

import sqlite3


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup our skeleton component."""
    old_states = [s.entity_id for s in hass.states.async_all() 
                  if s.entity_id.startswith(f"{DOMAIN}.")]
    for state in old_states:
        hass.states.async_remove(state)

    db = VoucherWalletDatabase(hass)  # Initialize the database
    hass.data[DOMAIN] = {"db": db}  # Store the database instance in hass.data for later use

    hass.http.register_view(AddVoucherView)
    hass.http.register_view(RemoveVoucherView)

    # Return boolean to indicate that initialization was successfully.
    return True