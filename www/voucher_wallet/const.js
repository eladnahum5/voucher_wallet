/// This file defines constants for the Voucher Wallet custom component in Home Assistant.

export const ITEM_PARAMETERS = {
    name: {
        type: "string",
        description: "Name of the item",
        required: true,
    },
    issuer: {
        type: "string",
        description: "Issuer of the item",
        required: true,
    },
    redeem_code: {
        type: "integer",
        description: "Unique item code",
        required: true,
    },
    code_type: {
        type: "string",
        description: "Type of the item code (e.g., qr, barcode)",
        required: true,
    },
    pin_code: {
        type: "integer",
        description: "PIN code for redeeming the item",
        required: false,
    },
    issue_date: {
        type: "string",
        description: "Date when the item was issued (ISO format)",
        required: true,
    },
    expiry_date: {
        type: "string",
        description: "Date when the item expires (ISO format)",
        required: false,
    },
    description: {
        type: "string",
        description: "Additional details about the item",
        required: false,
    },
    logo_slug: {
        type: "string",
        description: "Slug for the item's logo image",
        required: false,
    },
    value: {
        type: "float",
        description: "Monetary value of the item",
        required: true,
    },
};
