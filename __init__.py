DOMAIN = "voucher_wallet"

async def async_setup(hass, config):
    hass.states.async_set("voucher_wallet.version", "0.1.0")
    return True