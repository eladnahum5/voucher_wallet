// wallet.js — the main view: fetches and displays all vouchers
// Mirrors fetchAndDisplayVouchers() from voucher_wallet_card.js

import { fetchItems } from '../api.js';
import { createCard } from '../components/card.js';

export async function renderWallet(container) {
    // Show placeholder while loading (same as the HA card)
    container.innerHTML = '<p>Loading vouchers...</p>';

    // Refresh button — clicking it re-runs this whole function
    const refreshBtn = document.createElement('button');
    refreshBtn.textContent = 'Refresh vouchers';
    refreshBtn.addEventListener('click', () => renderWallet(container));

    const items = await fetchItems();

    container.innerHTML = '';
    container.appendChild(refreshBtn);

    // One card per voucher, same fields as the HA card
    items.forEach((item) => {
        container.appendChild(createCard(item));
    });
}
