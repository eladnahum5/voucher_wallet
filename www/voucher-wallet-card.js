// voucher-wallet-card.js
// Home Assistant Lovelace custom card for voucher_wallet integration
// Place this file in your Home Assistant config/www/ directory

class VoucherWalletCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.cards = [];
        this.loading = false;
        this.error = '';
    }

    connectedCallback() {
        this.render();
        this.fetchCards();
    }

    async fetchCards() {
        this.loading = true;
        this.error = '';
        this.render();
        try {
            const resp = await fetch('/api/voucher_wallet/vouchers');
            if (!resp.ok) throw new Error('Failed to fetch cards');
            this.cards = await resp.json();
        } catch (e) {
            this.error = e.message;
        }
        this.loading = false;
        this.render();
    }

    async addCard(e) {
        e.preventDefault();
        const form = e.target;
        const code = form.code.value;
        if (!code) return;
        try {
            const resp = await fetch('/api/voucher_wallet/add', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            if (!resp.ok) throw new Error('Failed to add card');
            form.reset();
            this.fetchCards();
        } catch (e) {
            this.error = e.message;
            this.render();
        }
    }

    async removeCard(code) {
        try {
            const resp = await fetch('/api/voucher_wallet/remove', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ code })
            });
            if (!resp.ok) throw new Error('Failed to remove card');
            this.fetchCards();
        } catch (e) {
            this.error = e.message;
            this.render();
        }
    }

    render() {
        const style = `
            .card { border: 1px solid #ccc; padding: 8px; margin: 4px; }
            .error { color: red; }
        `;
        let html = `<style>${style}</style>`;
        html += `<h3>Voucher Wallet</h3>`;
        if (this.loading) {
            html += `<div>Loading...</div>`;
        } else {
            if (this.error) html += `<div class='error'>${this.error}</div>`;
            html += `<div>`;
            if (this.cards.length === 0) {
                html += `<div>No cards found.</div>`;
            } else {
                this.cards.forEach(card => {
                    html += `<div class='card'>
                        <span>${card.code}</span>
                        <button onclick='this.getRootNode().host.removeCard("${card.code}")'>Remove</button>
                    </div>`;
                });
            }
            html += `</div>`;
            html += `<form id='add-card-form'>
                <input name='code' placeholder='Card code' required />
                <button type='submit'>Add Card</button>
            </form>`;
        }
        this.shadowRoot.innerHTML = html;
        const form = this.shadowRoot.getElementById('add-card-form');
        if (form) form.onsubmit = this.addCard.bind(this);
    }
}

customElements.define('voucher-wallet-card', VoucherWalletCard);

// Usage: Add <voucher-wallet-card></voucher-wallet-card> to your Lovelace dashboard via custom card (resources)
// Make sure to add this JS file as a resource in Home Assistant UI settings.
// example for Lovelace YAML:
/*
type: 'custom:voucher-wallet-card'
*/