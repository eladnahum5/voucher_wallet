from homeassistant.components.http import HomeAssistantView
from aiohttp import web

from .const import DOMAIN, VOUCHER_PARAMETERS

class AddVoucherView(HomeAssistantView):
    """View to add a voucher via HTTP POST."""

    url = f"/api/{DOMAIN}/add_voucher"
    name = f"api:{DOMAIN}:add_voucher"
    requires_auth = False # Only for testing, should be True in production

    async def get(self, request: web.Request) -> web.Response:
        """
        Handle GET requests.
        Expects voucher data as query parameters based on VOUCHER_PARAMETERS.
        """
        data = {}
        for param, details in VOUCHER_PARAMETERS.items():
            data[param] = request.query.get(param)
            if details["required"] and not data[param]:
                return self.json({"error": f"Missing required parameter: {param}"}, status=400)
        
        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].add_voucher(data)
        return self.json({"status": True})

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
        hass.data[DOMAIN]["db"].remove_voucher(int(code))
        return self.json({"status": True})
    
class ReinitializeDatabaseView(HomeAssistantView):
    """View to reinitialize the database via HTTP POST."""

    url = f"/api/{DOMAIN}/reinitialize_database"
    name = f"api:{DOMAIN}:reinitialize_database"
    requires_auth = False # Only for testing, should be True in production

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET requests."""
        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].reinitialize_database() 
        return self.json({"status": True})
        