import { ITEM_PARAMETERS } from "./const.js";

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