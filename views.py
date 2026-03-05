from homeassistant.components.http import HomeAssistantView
from aiohttp import web

from .const import DOMAIN

class AddVoucherView(HomeAssistantView):
    """View to add a voucher via HTTP POST."""

    url = f"/api/{DOMAIN}/add_voucher"
    name = f"api:{DOMAIN}:add_voucher"
    requires_auth = False # Only for testing, should be True in production

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET requests."""
        code = request.query.get("code")
        value = request.query.get("value")
        
        if not code or not value:
            return self.json({"error": "Missing code or value"}, status=400)
        
        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].add_voucher(int(code), float(value))
        return self.json({"status": True, "code": code, "value": value, "redeemed": False})

class RemoveVoucherView(HomeAssistantView):
    """View to remove a voucher via HTTP POST."""

    url = f"/api/{DOMAIN}/remove_voucher"
    name = f"api:{DOMAIN}:remove_voucher"
    requires_auth = False # Only for testing, should be True in production

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET requests."""
        code = request.query.get("code")

        if not code:
            return self.json({"error": "Missing code"}, status=400)
        
        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].remove_voucher(int(code))  # type: ignore
        return self.json({"status": True, "code": code})
        