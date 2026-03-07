// api.js — all calls to the Home Assistant backend live here

// HA stores the logged-in user's auth token in localStorage
function getToken() {
    const stored = localStorage.getItem('hassTokens');
    return stored ? JSON.parse(stored).access_token : null;
}

// Shared headers used in every request
function authHeaders() {
    return { Authorization: `Bearer ${getToken()}` };
}

// GET /api/voucher_wallet/items → returns the array of voucher objects
export async function fetchItems() {
    const response = await fetch('/api/voucher_wallet/items', {
        headers: authHeaders(),
    });
    const data = await response.json();
    return data.items;
}

// POST /api/voucher_wallet/items — creates a new voucher
// itemData must include: name, issuer, redeem_code, code_type, value, issue_date
export async function addItem(itemData) {
    await fetch('/api/voucher_wallet/items', {
        method: 'POST',
        headers: {
            ...authHeaders(),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(itemData),
    });
}
