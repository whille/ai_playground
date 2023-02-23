#!/usr/bin/env python
import aiohttp

class WsConnection:
    def __init__(self, url):
        self.url = url
        self.session = None
        self.ws = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        self.ws = await self.session.ws_connect(self.url)
        return self.ws

    async def __aexit__(self, exc_type, exc, tb):
        if self.ws is not None:
            await self.ws.close()
        if self.session is not None:
            await self.session.close()


class AWeb_Cient:
    def __init__(self, url):
        self.url = url

    async def on_message(self, message):
        pass

    async def send_heartbeat(self):
        pass

    async def start(self):
        pass

    def connect_ws(self):
        return WsConnection(self. url)

    async def handle_msg(self, ws):
        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                msg = self.on_message(msg.data)
                if msg:
                    yield msg
                    break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
