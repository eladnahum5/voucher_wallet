"""Config flow for Voucher Wallet integration."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries, exceptions
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({vol.Required("host"): str})

async def validate_input(hass: HomeAssistant, data: dict) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from the user input in the flow.
    """
    if len(data["host"]) < 3:
        raise InvalidHost
    return {"title": data["host"]}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Voucher Wallet."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
                return self.async_create_entry(title=info["title"], data=user_input)
            except InvalidHost:
                errors["base"] = "invalid_host"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
                
        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
            )
    
class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate the host is invalid."""