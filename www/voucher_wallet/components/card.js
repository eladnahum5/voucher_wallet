// card.js — builds one voucher card element
// Displays the same fields as the HA dashboard card in voucher_wallet_card.js

export function createCard(item) {
    const card = document.createElement('div');
    card.className = 'voucher-card';

    card.innerHTML = `
        <h3>${item.name}</h3>
        <p>Issuer: ${item.issuer}</p>
        <p>Value: $${item.value.toFixed(2)}</p>
        <p>Redeem code: ${item.redeem_code}</p>
        <p>Issue date: ${new Date(item.issue_date).toLocaleDateString()}</p>
    `;

    return card;
}
