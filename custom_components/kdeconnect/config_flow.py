import asyncio
import logging
import socket
import json
import time
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.components.zeroconf import ZeroconfServiceInfo

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

class KDEConnectConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_PUSH
    task_pairing: asyncio.Task | None = None
    discovery_info = None

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return await self.async_step_pair()

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({})
        )

    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo):
        self.discovery_info = discovery_info

        properties = self.discovery_info.properties
        device_id = properties.get("id")
        device_name = properties.get("name")
        _LOGGER.debug(f"[{device_name}] Discovered KDE Connect device")

        await self.async_set_unique_id(device_id)
        self._abort_if_unique_id_configured()

        self.context.update({
            "title_placeholders": {
                "name": device_name
            }
        })

        return await self.async_step_confirm()

    async def async_step_confirm(self, user_input=None):
        properties = self.discovery_info.properties
        device_name = properties.get("name")

        return self.async_show_form(
            step_id="pair",
            description_placeholders={"name": device_name},
            data_schema=vol.Schema({}),
            errors={"abort": "pairing_failed"}
        )

    async def async_step_pair(self, user_input=None):
        properties = self.discovery_info.properties
        device_id = properties.get("id")
        device_name = properties.get("name")

        await self.async_set_unique_id(device_id)
        self._abort_if_unique_id_configured()

        if not self.task_pairing:
            _LOGGER.debug(f"[{device_name}] Pairing KDE Connect device")
            coro = self._send_pair_request(device_id)
            self.task_pairing = self.hass.async_create_task(coro)
            return self.async_show_progress(
                progress_action="task_pairing",
                progress_task=self.task_pairing,
                description_placeholders={"name": device_name}
            )

        _LOGGER.debug(f"[{device_name}] Waiting for Pairing Response from KDE Connect device")
        # Send pair request
        success = self.task_pairing.result()

        _LOGGER.debug(f"[{device_name}] Pairing successful: {success}")

        if success:
            _LOGGER.debug(f"[{device_name}] Creating entry for KDE Connect device")
            return self.async_show_progress_done(next_step_id="finish")
        else:
            _LOGGER.debug(f"[{device_name}] Pairing failed")
            return self.async_show_progress_done(next_step_id="failed")


    async def async_step_finish(self, user_input=None):
        properties = self.discovery_info.properties
        device_id = properties.get("id")
        device_name = properties.get("name")
        return self.async_create_entry(
            title=device_name,
            data={"device_id": device_id, "device_name": device_name}
        )

    async def async_step_failed(self, user_input=None):
        return self.async_abort(reason="pairing_failed")

    async def _send_pair_request(self, device_id):
        properties = self.discovery_info
        device_name = properties.name
        device_address = properties.host
        device_port = properties.port

        _LOGGER.debug(f"[{device_name}] Sending Pairing Request to KDE Connect device at {device_address}:{device_port}")

        identify_payload = {
            "id": f"_{int(time.time())}_",
            "type": "kdeconnect.identify",
            "body": {
                "deviceId": "740bd4b9_b418_4ee4_97d6_caf1da8151be",
                "deviceName": "Home Assistant",
                "deviceType": "desktop",
                "incomingCapabilities": [
                    "kdeconnect.mock.echo",
                ],
                "outgoingCapabilities": [
                    "kdeconnect.mock.echo",
                ],
                "protocolVersion": 7
            }
        }
        # Create the pairing request payload
        pairing_payload = {
            "id": f"_{int(time.time())}_",
            "type": "kdeconnect.pair",
            "body": {
                "pair": True
            }
        }

        # Serialize the payload to JSON
        identify_payload_json = json.dumps(identify_payload)
        pairing_payload_json = json.dumps(pairing_payload)

        # Send the UDP packet
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.sendto(identify_payload_json.encode('utf-8'), (device_address, device_port))
            sock.sendto(pairing_payload_json.encode('utf-8'), (device_address, device_port))

        # Wait for the response (This is simulated, replace with actual response handling)
        await asyncio.sleep(5)  # Simulate network delay

        # Simulated response, replace with actual response handling
        response = {"body": {"pair": False}}
        _LOGGER.debug(f"[{device_name}] Got Pairing Response from KDE Connect device: {response}")
        return response["body"].get("pair", False)
