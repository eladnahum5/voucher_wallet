"""This module defines constants for the voucher_wallet custom component in Home Assistant."""

DOMAIN = "voucher_wallet"
TABLE_NAME = "items"

ITEM_PARAMETERS = {
    "name": {"type": "string", "description": "Name of the item", "required": True},
    "issuer": {
        "type": "string",
        "description": "Issuer of the item",
        "required": True,
    },
    "redeem_code": {
        "type": "integer",
        "description": "Unique item code",
        "required": True,
    },
    "code_type": {
        "type": "string",
        "description": "Type of the item code (e.g., qr, barcode)",
        "required": True,
    },
    "pin_code": {
        "type": "integer",
        "description": "PIN code for redeeming the item",
        "required": False,
    },
    "issue_date": {
        "type": "string",
        "description": "Date when the item was issued (ISO format)",
        "required": True,
    },
    "expiry_date": {
        "type": "string",
        "description": "Date when the item expires (ISO format)",
        "required": False,
    },
    "description": {
        "type": "string",
        "description": "Additional details about the item",
        "required": False,
    },
    "logo_slug": {
        "type": "string",
        "description": "Slug for the item's logo image",
        "required": False,
    },
    "value": {
        "type": "float",
        "description": "Monetary value of the item",
        "required": True,
    },
}
