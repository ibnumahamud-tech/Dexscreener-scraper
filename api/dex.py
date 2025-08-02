import asyncio
import base64
import os
from curl_cffi.requests import AsyncSession
import json
import nest_asyncio
from datetime import datetime
import time
import struct
from decimal import Decimal, ROUND_DOWN
import re
import requests

# Apply nest_asyncio
nest_asyncio.apply()

Api = "TG bot API here"
ID = "Channel ID"

class DexBot:
    def __init__(self, api_key, url, channel_id=ID, max_token=10):
        self.api_key = api_key
        self.channel_id = channel_id
        self.max_token = max_token
        self.url = url

    def generate_sec_websocket_key(self):
        random_bytes = os.urandom(16)
        key = base64.b64encode(random_bytes).decode("utf-8")
        return key

    def get_headers(self):
        return {
            "Host": "io.dexscreener.com",
            "Connection": "Upgrade",
            "User-Agent": "...",
            "Upgrade": "websocket",
            "Origin": "https://dexscreener.com",
            "Sec-WebSocket-Version": "13",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-WebSocket-Key": self.generate_sec_websocket_key(),
        }

    def format_token_data(self):
        token_addresses = self.start()
        base_url = "https://api.dexscreener.com/latest/dex/tokens/"
        results = {}
        for address in token_addresses:
            try:
                resp = requests.get(f"{base_url}{address}")
                if resp.status_code == 200:
                    data = resp.json()
                    pairs = data.get("pairs", [])
                    results[address] = pairs[0] if pairs else {
                        "pairAddress": address,
                        "Error": "No data Retrieved"
                    }
                else:
                    results[address] = f"Error: Status code {resp.status_code}"
            except Exception as e:
                results[address] = f"Error making request: {e}"
        return json.dumps({"data": list(results.values())}, indent=2)

    async def connect(self):
        headers = self.get_headers()
        try:
            session = AsyncSession(headers=headers)
            ws = await session.ws_connect(self.url)
            while True:
                data = await ws.recv()
                if data and "pairs" in str(data[0]):
                    return data[0]
            await ws.close()
            await session.close()
        except Exception as e:
            return f"Connection error: {e}"

    def tg_send(self, message):
        try:
            self.bot.send_message(
                self.channel_id,
                message,
                parse_mode="MarkdownV2",
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"Telegram sending error: {e}")

    def start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        mes = loop.run_until_complete(self.connect())
        loop.close()

        # Decode safely
        if isinstance(mes, (bytes, bytearray)):
            decoded_text = "".join(
                chr(b) if 32 <= b <= 126 else " " for b in mes
            )
        elif isinstance(mes, str):
            decoded_text = mes
        else:
            decoded_text = str(mes)

        words = [w for w in decoded_text.split() if len(w) >= 55]
        filtered = [re.sub(r'["*<$@(),.].*', "", w) for w in words]

        extracted = []
        for token in filtered:
            try:
                if "0x" in token:
                    token = re.findall(r"(0x[0-9a-fA-F]+)", token)[-1]
                elif "pump" in token:
                    token = re.findall(r".{0,40}pump", token)[0].lstrip("V")
                else:
                    token = token[-44:]
                extracted.append(token)
            except Exception:
                pass

        return extracted[: self.max_token]

    def token_getter(self, message):
        pass


def get_tokens(blockchain="Solana", max_token=60):
    url = f"wss://io.dexscreener.com/dex/screener/v1/stream/trending?chainIds=%5B%22{blockchain.lower()}%22%5D"
    bot = DexBot(api_key="", url=url, channel_id="", max_token=max_token)
    json_str = bot.format_token_data()
    data = json.loads(json_str)["data"]
    return data[:max_token]

    # 3) Scrape & format
    json_str = bot.format_token_data()
    data = json.loads(json_str)["data"]
    # 4) Return up to max_token entries as a list of dicts
    return data[:max_token]




