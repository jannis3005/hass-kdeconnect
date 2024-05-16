from homeassistant.helpers import discovery

async def async_setup(hass, config):
    return True

async def async_setup_entry(hass, entry):
    hass.async_create_task(discovery.async_load_platform(
        hass, "sensor", DOMAIN, {}, entry.config
    ))
    return True

async def async_unload_entry(hass, entry):
    return True