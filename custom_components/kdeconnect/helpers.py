import asyncio
import aiohttp

async def send_pair_request(device_ip, device_port):
    pair_url = f"http://{device_ip}:{device_port}/pair"
    async with aiohttp.ClientSession() as session:
        async with session.post(pair_url, json={"type": "kdeconnect.pair", "body": {"pair": True}}) as response:
            if response.status == 200:
                response_data = await response.json()
                return response_data.get("body", {}).get("pair", False)
    return False