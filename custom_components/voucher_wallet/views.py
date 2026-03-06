from homeassistant.components.http import HomeAssistantView
from aiohttp import web

from .const import DOMAIN, VOUCHER_PARAMETERS

class AddVoucherView(HomeAssistantView):
    """View to add a voucher via HTTP POST."""

    url = f"/api/{DOMAIN}/add_voucher"
    name = f"api:{DOMAIN}:add_voucher"
    requires_auth = False # Only for testing, should be True in production

    async def post(self, request: web.Request) -> web.Response:
        """
        Expects voucher data as query parameters based on VOUCHER_PARAMETERS.
        """
        try:
            body = await request.json()
        except Exception:
                return self.json({"error": "Invalid JSON in request body"}, status=400)

        for key in body.keys():
            if key not in VOUCHER_PARAMETERS:
                return self.json({"error": f"Unexpected parameter: {key}"}, status=400)

        for param, details in VOUCHER_PARAMETERS.items():
            if details["required"] and not body.get(param):
                return self.json({"error": f"Missing required parameter: {param}"}, status=400)
        
        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].add_voucher(body)
        return self.json({"status": True})

class RemoveVoucherView(HomeAssistantView):
    """View to remove a voucher via HTTP POST."""

    url = f"/api/{DOMAIN}/remove_voucher"
    name = f"api:{DOMAIN}:remove_voucher"
    requires_auth = False # Only for testing, should be True in production

    async def post(self, request: web.Request) -> web.Response:
        """Expects a 'code' query parameter to identify the voucher to remove."""
        try:
            body = await request.json()
        except Exception:
            return self.json({"error": "Invalid JSON in request body"}, status=400)

        code = body.get("code")

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

    async def delete(self, request: web.Request) -> web.Response:
        """Reinitializes the database by dropping and recreating the vouchers table."""
        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].reinitialize_database() 
        return self.json({"status": True})
        
class GetAllVouchersView(HomeAssistantView):
    """View to retrieve all vouchers via HTTP GET."""

    url = f"/api/{DOMAIN}/get_all_vouchers"
    name = f"api:{DOMAIN}:get_all_vouchers"
    requires_auth = False # Only for testing, should be True in production

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET requests."""
        hass = request.app["hass"]
        vouchers = hass.data[DOMAIN]["db"].get_all_vouchers()
        return self.json({"vouchers": vouchers})