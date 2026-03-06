// Define the parameters for the voucher wallet items
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

class VoucherWalletCard extends HTMLElement {
    // Define properties for the card
    // it must be here because we need to access it in both setConfig and set hass methods
    config;
    content;

    // This method is called when the card is added to the DOM
    // DOM is the Document Object Model, which represents the structure of a web page
    setConfig(config) {
        this.config = config;
    }

    // Display the vouchers in the card
    async displayVouchers() {
        const vouchers = await this.config.hass.callApi("GET", "/api/voucher_wallet/items");
        this.content.innerHTML = '';
        if (vouchers.length === 0) {
            this.content.innerHTML = '<p>No vouchers available.</p>';
            return;
        }
        vouchers.forEach(voucher => {
            const voucherElement = document.createElement('div');
            voucherElement.classList.add('voucher');
            voucherElement.innerHTML = `
                <h3>${voucher.name}</h3>
                <p><strong>Issuer:</strong> ${voucher.issuer}</p>
                <p><strong>Redeem Code:</strong> ${voucher.redeem_code}</p>
            `;
            this.content.appendChild(voucherElement);
        });
    }
}

// Register the custom element with the browser
customElements.define('voucher-wallet-card', VoucherWalletCard);

// This code adds the custom card to the list of available cards in Home Assistant,
// allowing users to select it when configuring their dashboards
window.customCards = window.customCards || [];
window.customCards.push({
    type: 'voucher-wallet-card',
    name: 'Voucher Wallet Card',
    description: 'A custom card for displaying voucher wallet information.',
});