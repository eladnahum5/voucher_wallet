// add.js — the add-voucher form
// Mirrors addVoucher() from voucher_wallet_card.js

import { addItem } from '../api.js';

// Renders the form into `container`.
// `onAdded` is called after a successful submission so the wallet list can refresh.
export function renderAddForm(container, onAdded) {
    // Only the required fields from ITEM_PARAMETERS are shown here
    container.innerHTML = `
        <form id="add-form">
            <input name="name"        placeholder="Name"            required />
            <input name="issuer"      placeholder="Issuer"          required />
            <input name="redeem_code" placeholder="Redeem code" type="number" required />
            <input name="code_type"   placeholder="Code type (e.g. qr, barcode)" required />
            <input name="value"       placeholder="Value"       type="number" step="0.01" required />
            <input name="issue_date"  placeholder="Issue date"  type="date"   required />
            <button type="submit">Add voucher</button>
        </form>
    `;

    container.querySelector('#add-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        const form = new FormData(e.target);

        await addItem({
            name:        form.get('name'),
            issuer:      form.get('issuer'),
            redeem_code: Number(form.get('redeem_code')),
            code_type:   form.get('code_type'),
            value:       Number(form.get('value')),
            issue_date:  form.get('issue_date'),
        });

        onAdded(); // tell the caller (app.js) to refresh the wallet list
    });
}
