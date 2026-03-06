DOMAIN = "voucher_wallet"

VOUCHER_PARAMETERS = {
    "name": {
        "type": "string",
        "description": "Name of the voucher",
        "required": True
    },
    "issuer": {
        "type": "string",
        "description": "Issuer of the voucher",
        "required": True
    },
    "redeem_code": {
        "type": "integer",
        "description": "Unique voucher code",
        "required": True   
    },
    "code_type": {
        "type": "string",
        "description": "Type of the voucher code (e.g., qr, barcode)",
        "required": True
    },
    "pin_code": {
        "type": "integer",
        "description": "PIN code for redeeming the voucher",
        "required": False
    },
    "issue_date": {
        "type": "string",
        "description": "Date when the voucher was issued (ISO format)",
        "required": True
    },
    "expiry_date": {
        "type": "string",
        "description": "Date when the voucher expires (ISO format)",
        "required": False
    },
    "description": {
        "type": "string",
        "description": "Additional details about the voucher",
        "required": False
    },
    "logo_slug": {
        "type": "string",
        "description": "Slug for the voucher's logo image",
        "required": False
    },
    "value": {
        "type": "float",
        "description": "Monetary value of the voucher",
        "required": True
    }
}