from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup(hass: HomeAssistant, config: dict):
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    return True
