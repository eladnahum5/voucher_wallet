# most basic 1 state init file for voucher_wallet domain for Home Assistant
from .const import DOMAIN

async def async_setup_entry(hass, entry):
    """Set up the Hello, state! config entry."""
    # This is where you would set up your integration, e.g. by creating an instance of your main class and adding it to hass.data
    # For example:
    hass.state.set(f"{DOMAIN}.state", "Hello, state!")
    return True