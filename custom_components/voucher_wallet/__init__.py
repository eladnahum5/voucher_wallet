from __future__ import annotations

from homeassistant.const import EVENT_HOMEASSISTANT_STARTED
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from homeassistant.setup import async_setup_component

from .const import DOMAIN
from .sqlite_helper import VoucherWalletDatabase
from .views import AddVoucherView, GetAllVouchersView, ReinitializeDatabaseView, RemoveVoucherView

CARD_URL = "/local/community/voucher_wallet/voucher-wallet-card.js"


async def _async_register_lovelace_resource(hass: HomeAssistant) -> None:
    """Add the card JS as a Lovelace resource if not already registered."""
    try:
        await async_setup_component(hass, "lovelace", {})
        resources = hass.data.get("lovelace", {}).get("resources")
        if resources is None:
            return
        await resources.async_load()
        if any(r.get("url") == CARD_URL for r in resources.async_items()):
            return
        await resources.async_create_item({"res_type": "module", "url": CARD_URL})
    except Exception:
        pass  # yaml-mode Lovelace or resource collection unavailable


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
    hass.http.register_view(ReinitializeDatabaseView)
    hass.http.register_view(GetAllVouchersView)

    async def on_started(_event):
        await _async_register_lovelace_resource(hass)

    hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STARTED, on_started)

    # Return boolean to indicate that initialization was successful.
    return True