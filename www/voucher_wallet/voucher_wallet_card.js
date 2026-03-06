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

    // Read all vouchers using GET request to the API endpoint /api/voucher_wallet/get_all_vouchers
    async getVouchers() {
        const response = await fetch('/api/voucher_wallet/get_all_vouchers');
        if (!response.ok) {
            throw new Error('Failed to fetch vouchers');
        }
        return await response.json();
    }

    // Display the vouchers in the card
    async displayVouchers() {
        const vouchers = await this.getVouchers();
        this.content.innerHTML = '';
        vouchers.forEach(voucher => {
            const voucherElement = document.createElement('div');
            voucherElement.classList.add('voucher');
            voucherElement.innerHTML = `
                <h3>${voucher.name}</h3>
                <p>Value: ${voucher.value}</p>
                <p>Expiry: ${voucher.expiry}</p>
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