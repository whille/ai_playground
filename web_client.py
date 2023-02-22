#!/usr/bin/env python

import asyncio
import aiohttp


class AWeb_Cient:
    def __init__(self, url):
        self.url = url
        self.session = None
        self.ws = None

    async def on_message(self, message):
        pass

    async def send_heartbeat(self):
        pass

    async def start(self):
        pass

    async def heartbeat(self):
        while True:
            try:
                await self.send_heartbeat()
                await asyncio.sleep(10)
            except (aiohttp.ClientError, asyncio.CancelledError):
                break

    async def connect(self):
        if not self.ws:
            self.session = aiohttp.ClientSession()
            self.ws = await self.session.ws_connect(self.url, heartbeat=5)

    async def run(self):
        async for msg in self.ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                yield self.on_message(msg.data)
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
        await self.on_close()

    async def on_close(self):
        await self.session.close()
        self.ws = None
