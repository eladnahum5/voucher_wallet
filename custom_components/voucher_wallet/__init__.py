"""This is the __init__.py file for the voucher_wallet custom component in Home Assistant."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN
from .sqlite_helper import VoucherWalletDatabase
from .views import ItemIdView, ItemView, ReinitializeDatabaseView


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup our skeleton component."""

    db = VoucherWalletDatabase(hass)  # Initialize the database
    hass.data[DOMAIN] = {"db": db}

    hass.http.register_view(ItemView)
    hass.http.register_view(ItemIdView)
    hass.http.register_view(ReinitializeDatabaseView)

    return True
