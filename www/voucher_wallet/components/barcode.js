// barcode.js — displays a redeem code
// The reference card shows the code as plain text, so we do the same here

export function createBarcodeDisplay(code) {
    const el = document.createElement('span');
    el.className = 'redeem-code';
    el.textContent = code;
    return el;
}
