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

    // This method is called when the card is updated with new data
    set hass(hass) {
        this._hass = hass;

        // If the content element doesn't exist, create it
        if (!this.content) {
            // add placeholder content to the card while we fetch the data
            this.content = document.createElement('div');
            this.content.innerHTML = '<p>Loading vouchers...</p>';
            this.appendChild(this.content);
        }

        // Data refresh button
        if (!this.refreshButton) {
            this.refreshButton = document.createElement('button');
            this.refreshButton.textContent = 'Refresh Vouchers';
            this.refreshButton.addEventListener('click', () => {
                this.fetchAndDisplayVouchers();
            });
            this.content.appendChild(this.refreshButton);
        }

        // Fetch and display the vouchers when the card is updated
        this.fetchAndDisplayVouchers();
    }

    // Method to add vouchers (form submission)
    async addVoucher(voucherData) {
        try {
            const response = await this._hass.callApi('POST', 'voucher_wallet/items', voucherData);
            console.log('Voucher added successfully:', response);
            // Refresh the voucher list after adding a new voucher
            this.fetchAndDisplayVouchers();
        } catch (error) {
            console.error('Error adding voucher:', error);
        }
    }


    // Method to fetch voucher items from the API and display them in the card
    async fetchAndDisplayVouchers() {

        // Display the vouchers in the card
        console.log('Fetching voucher items from API...');
        const data = await this._hass.callApi('GET', 'voucher_wallet/items');
        console.log('Received voucher data:', data);

        // Clear previous content
        this.content.innerHTML = '';
        if (this.refreshButton) {
            this.content.appendChild(this.refreshButton);
        }

        // Create a card for each voucher item
        data.items.forEach(item => {
            console.log('Displaying voucher item:', item);
            const itemCard = document.createElement('div');
            itemCard.classList.add('voucher-item');

            itemCard.innerHTML = `
                <h3>${item.name}</h3>
                <p>Issuer: ${item.issuer}</p>
                <p>Value: $${item.value.toFixed(2)}</p>
                <p>Redeem Code: ${item.redeem_code}</p>
                <p>Issue Date: ${new Date(item.issue_date).toLocaleDateString()}</p>
            `;

            this.content.appendChild(itemCard);
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