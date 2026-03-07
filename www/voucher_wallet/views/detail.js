// detail.js — shows all fields of a single voucher
// Displays the same fields as the card view (no extra logic beyond the reference)

export function renderDetail(container, item) {
    container.innerHTML = `
        <h2>${item.name}</h2>
        <p>Issuer: ${item.issuer}</p>
        <p>Value: $${item.value.toFixed(2)}</p>
        <p>Redeem code: ${item.redeem_code}</p>
        <p>Issue date: ${new Date(item.issue_date).toLocaleDateString()}</p>
    `;
}
