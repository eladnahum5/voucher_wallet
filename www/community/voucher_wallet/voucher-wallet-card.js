class VoucherWalletCard extends HTMLElement {
  setConfig(config) {
    this._config = config;
  }

  getCardSize() {
    return 3;
  }

  connectedCallback() {
    if (!this.shadowRoot) {
      this.attachShadow({ mode: "open" });
    }
    this._render();
    this._loadVouchers();
  }

  _render() {
    this.shadowRoot.innerHTML = `
      <style>
        :host { display: block; }
        ha-card { padding: 16px; }
        h2 { margin: 0 0 16px; font-size: 1.2em; }
        .voucher {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 8px 0;
          border-bottom: 1px solid var(--divider-color, #e0e0e0);
        }
        .voucher:last-child { border-bottom: none; }
        .voucher-info { flex: 1; }
        .voucher-name { font-weight: bold; }
        .voucher-detail { font-size: 0.85em; color: var(--secondary-text-color, #888); }
        button {
          background: var(--primary-color, #03a9f4);
          color: white;
          border: none;
          border-radius: 4px;
          padding: 6px 12px;
          cursor: pointer;
          font-size: 0.85em;
        }
        button.remove {
          background: var(--error-color, #db4437);
        }
        .empty { color: var(--secondary-text-color, #888); font-style: italic; }
        details { margin-top: 16px; }
        summary { cursor: pointer; font-weight: bold; padding: 4px 0; }
        .form { display: flex; flex-direction: column; gap: 8px; margin-top: 12px; }
        .form input {
          padding: 6px 8px;
          border: 1px solid var(--divider-color, #ccc);
          border-radius: 4px;
          background: var(--card-background-color, white);
          color: var(--primary-text-color, black);
          font-size: 0.9em;
        }
        .form label { font-size: 0.85em; margin-bottom: -4px; }
        .form button { align-self: flex-start; }
        .error { color: var(--error-color, #db4437); font-size: 0.85em; margin-top: 4px; }
      </style>
      <ha-card>
        <h2>Voucher Wallet</h2>
        <div id="voucher-list"><span class="empty">Loading...</span></div>
        <details>
          <summary>Add Voucher</summary>
          <div class="form">
            <label>Name *</label>
            <input id="name" type="text" placeholder="e.g. Coffee Shop" />
            <label>Issuer *</label>
            <input id="issuer" type="text" placeholder="e.g. Starbucks" />
            <label>Redeem Code *</label>
            <input id="redeem_code" type="number" placeholder="e.g. 123456" />
            <label>Code Type *</label>
            <input id="code_type" type="text" placeholder="e.g. barcode, qr" />
            <label>Issue Date * (YYYY-MM-DD)</label>
            <input id="issue_date" type="date" />
            <label>Value *</label>
            <input id="value" type="number" step="0.01" placeholder="e.g. 10.00" />
            <label>Expiry Date (YYYY-MM-DD)</label>
            <input id="expiry_date" type="date" />
            <label>Description</label>
            <input id="description" type="text" placeholder="Optional description" />
            <div id="form-error" class="error"></div>
            <button id="add-btn">Add Voucher</button>
          </div>
        </details>
      </ha-card>
    `;

    this.shadowRoot.getElementById("add-btn").addEventListener("click", () => this._submitForm());
  }

  async _loadVouchers() {
    try {
      const resp = await fetch("/api/voucher_wallet/get_all_vouchers");
      const data = await resp.json();
      this._displayVouchers(data.vouchers || []);
    } catch (e) {
      this.shadowRoot.getElementById("voucher-list").innerHTML =
        '<span class="error">Failed to load vouchers.</span>';
    }
  }

  _displayVouchers(vouchers) {
    const list = this.shadowRoot.getElementById("voucher-list");
    if (!vouchers.length) {
      list.innerHTML = '<span class="empty">No vouchers yet.</span>';
      return;
    }
    list.innerHTML = vouchers
      .map(
        (v) => `
        <div class="voucher">
          <div class="voucher-info">
            <div class="voucher-name">${this._esc(v.name)} — ${this._esc(String(v.value))}</div>
            <div class="voucher-detail">${this._esc(v.issuer)} · Code: ${this._esc(String(v.redeem_code))} · ${this._esc(v.code_type)}</div>
            ${v.expiry_date ? `<div class="voucher-detail">Expires: ${this._esc(v.expiry_date)}</div>` : ""}
          </div>
          <button class="remove" data-code="${v.redeem_code}">Remove</button>
        </div>
      `
      )
      .join("");

    list.querySelectorAll("button.remove").forEach((btn) => {
      btn.addEventListener("click", () => this._removeVoucher(btn.dataset.code));
    });
  }

  async _submitForm() {
    const get = (id) => this.shadowRoot.getElementById(id).value.trim();
    const errorEl = this.shadowRoot.getElementById("form-error");
    errorEl.textContent = "";

    const payload = {
      name: get("name"),
      issuer: get("issuer"),
      redeem_code: parseInt(get("redeem_code"), 10),
      code_type: get("code_type"),
      issue_date: get("issue_date"),
      value: parseFloat(get("value")),
    };

    const expiry = get("expiry_date");
    if (expiry) payload.expiry_date = expiry;
    const desc = get("description");
    if (desc) payload.description = desc;

    if (!payload.name || !payload.issuer || isNaN(payload.redeem_code) || !payload.code_type || !payload.issue_date || isNaN(payload.value)) {
      errorEl.textContent = "Please fill in all required fields.";
      return;
    }

    try {
      const resp = await fetch("/api/voucher_wallet/add_voucher", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      const data = await resp.json();
      if (!resp.ok) {
        errorEl.textContent = data.error || "Failed to add voucher.";
        return;
      }
      ["name", "issuer", "redeem_code", "code_type", "issue_date", "value", "expiry_date", "description"].forEach(
        (id) => (this.shadowRoot.getElementById(id).value = "")
      );
      this._loadVouchers();
    } catch (e) {
      errorEl.textContent = "Network error.";
    }
  }

  async _removeVoucher(code) {
    try {
      await fetch("/api/voucher_wallet/remove_voucher", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: parseInt(code, 10) }),
      });
      this._loadVouchers();
    } catch (e) {
      // silently fail
    }
  }

  _esc(str) {
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }
}

customElements.define("voucher-wallet-card", VoucherWalletCard);
