"""
The "hello world" custom component.

This component implements the bare minimum that a component should implement.

Configuration:

To use the hello_world component you will need to add the following to your
configuration.yaml file.

voucher_wallet:
"""
from __future__ import annotations

import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

@asyncio.coroutine
def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Setup our skeleton component."""
    # States are in the format DOMAIN.OBJECT_ID.
    hass.states.async_set('voucher_wallet.Hello_World', 'Works!')

    # Return boolean to indicate that initialization was successfully.
    return True
