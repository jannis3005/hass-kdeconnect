import asyncio
import logging
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.zeroconf import ZeroconfServiceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class KDEConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH

    def __init__(self):
        self.discovery_info = None

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return await self.async_step_pair()

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({})
        )

    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo):
        _LOGGER.debug(f"Discovered KDE Connect device: {discovery_info}")
        self.discovery_info = discovery_info
        return await self.async_step_pair()

    async def async_step_pair(self, user_input=None):
        if not self.discovery_info:
            return self.async_abort(reason="no_discovery_info")

        # Extracting device info from the discovery_info
        device_name = self.discovery_info.name
        properties = self.discovery_info.properties
        device_id = properties.get("id")
        protocol_version = properties.get("protocol")
        device_type = properties.get("type")

        if not device_id or not device_name:
            return self.async_abort(reason="missing_device_info")

        # Send pair request
        success = await self._send_pair_request(device_id)

        if success:
            return self.async_create_entry(
                title=device_name, data={"device_id": device_id, "device_name": device_name}
            )
        else:
            return self.async_abort(reason="pairing_failed")

    async def _send_pair_request(self, device_id):
        # Mock function to send a pair request and wait for a response
        # Replace this with actual logic to communicate with the KDE Connect device
        await asyncio.sleep(1)  # Simulate network delay

        # Simulated response, replace with actual response handling
        response = {"body": {"pair": True}}
        return response["body"].get("pair", False)
