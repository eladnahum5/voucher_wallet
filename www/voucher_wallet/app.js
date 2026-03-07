// app.js — entry point, wires the views together

import { renderWallet } from './views/wallet.js';
import { renderAddForm } from './views/add.js';

const walletContainer = document.getElementById('wallet');
const addContainer    = document.getElementById('add');

// When a voucher is added, refresh the wallet list
function refresh() {
    renderWallet(walletContainer);
}

renderAddForm(addContainer, refresh);
refresh(); // load the wallet on page open
