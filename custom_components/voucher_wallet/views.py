"""This module defines the HTTP views for the voucher_wallet custom component in Home Assistant."""

from aiohttp import web

from homeassistant.components.http import HomeAssistantView

from .const import DOMAIN, ITEM_PARAMETERS


class ItemView(HomeAssistantView):
    """View to add an item via HTTP POST."""

    url = f"/api/{DOMAIN}/items"
    name = f"api:{DOMAIN}:items"
    requires_auth = True

    async def get(self, request: web.Request) -> web.Response:
        """Handle GET requests to retrieve all items."""
        hass = request.app["hass"]
        items = hass.data[DOMAIN]["db"].fetch_items()
        return self.json({"items": items})

    async def post(self, request: web.Request) -> web.Response:
        """Expects item data as query parameters based on ITEM_PARAMETERS."""
        try:
            body = await request.json()
        except ValueError:
            return self.json({"error": "Invalid JSON in request body"}, status=400)

        for key in body:
            if key not in ITEM_PARAMETERS:
                return self.json({"error": f"Unexpected parameter: {key}"}, status=400)

        for param, details in ITEM_PARAMETERS.items():
            if details["required"] and not body.get(param):
                return self.json(
                    {"error": f"Missing required parameter: {param}"}, status=400
                )

        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].insert_item(body)
        return self.json({"status": True})


class ReinitializeDatabaseView(HomeAssistantView):
    """View to reinitialize the database via HTTP POST."""

    url = f"/api/{DOMAIN}/reinitialize_database"
    name = f"api:{DOMAIN}:reinitialize_database"
    requires_auth = False  # Only for testing, should be True in production

    async def delete(self, request: web.Request) -> web.Response:
        """Reinitializes the database by dropping and recreating the vouchers table."""
        hass = request.app["hass"]
        hass.data[DOMAIN]["db"].reinitialize_database()
        return self.json({"status": True})
