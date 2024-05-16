from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

async def async_setup(hass: HomeAssistant, config: dict):
    # This function can be used to perform setup tasks that are necessary when Home Assistant starts
    # You might not need this if you're only handling config flow and discovery initially
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    # This function is called when an entry is being set up
    # You can initialize your integration here, if needed
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    # This function is called when an entry is being unloaded
    # You can clean up resources here, if needed
    return True
