#!/usr/bin/env python

import json
import uuid
import toml
import asyncio
from utils import logger
from aip import AipSpeech
from web_client import AWeb_Cient


# https://ai.baidu.com/ai-doc/SPEECH/2k5dllqxj#demo
# https://github.com/Baidu-AIP/speech-demo/blob/master/rest-api-asr/python/asr_json.py
# https://github.com/Baidu-AIP/speech-demo/blob/master/rest-api-tts/python/tts.py

URI = "ws://vop.baidu.com/realtime_asr"


class Baidu_Voice(AWeb_Cient):

    def __init__(self):
        self.cfg = toml.load('/etc/baidu.toml')['speech']
        uri = URI + "?sn=" + str(uuid.uuid1())
        logger.info(f"uri: {uri}, cfg: {self.cfg}")
        super(Baidu_Voice, self).__init__(uri)
        cfg = toml.load('/etc/baidu.toml')['speech']
        self.speaker = AipSpeech(cfg['APP_ID'], cfg['APP_KEY'], cfg['SECRET_KEY'])

    async def send_start_params(self, dev_pid=15372):
        req = {
            "type": "START",
            "data": {
                "appid": int(self.cfg['APP_ID']),
                "appkey": self.cfg['APP_KEY'],
                "dev_pid": dev_pid,  # 识别模型
                "cuid":
                    "yourself_defined_user_id",  # 随便填不影响使用。机器的mac或者其它唯一id，百度计算UV用。
                "sample": 16000,  # 固定参数
                "format": "pcm"  # 固定参数
            }
        }
        await self.ws.send_json(req)

    async def send_heartbeat(self):
        await self.ws.send_json({"type": "HEARTBEAT"})

    async def recognize(self, audo):
        async with self.connect_ws() as ws:
            await self.send_start_params()
            await self.send_audio(audo, 3000)
            await self.send_finish()
            return await self.handle_msg(ws)

    async def send_audio(self, pcm, chunk_ms=5000):
        """
        发送二进制音频数据，注意每个帧之间需要有间隔时间
        """
        chunk_len = int(16000 * 2 / 1000 * chunk_ms)
        total = len(pcm)
        logger.info("send_audio total={}".format(total))
        index = 0
        while index < total:
            end = index + chunk_len
            if end >= total:
                # 最后一个音频数据帧
                end = total
            body = pcm[index:end]
            logger.debug(
                "try to send audio length {}, from bytes [{},{})".format(
                    len(body), index, end))
            await self.ws.send_bytes(body)
            index = end
            await asyncio.sleep(chunk_ms / 1000.0)

    def on_message(self, message):
        logger.info(f"Response: {message}, {type(message)}")
        res = json.loads(message)
        if res.get('type') == 'HEARTBEAT':
            pass
        elif res.get("err_msg") != "OK":
            logger.error(res)
        elif res.get('type') == 'FIN_TEXT':
            return res.get('result', '')

    async def send_finish(self):
        await self.ws.send_json({"type": "FINISH"})

    async def send_cancel(self):
        await self.ws.send_json({"type": "CANCEL"})


async def main():
    import sys
    pcm_file = sys.argv[1]
    client = Baidu_Voice()
    with open(pcm_file, 'rb') as f:
        pcm = f.read()
        res = await client.recognize(pcm)
        print(res)


if __name__ == '__main__':
    asyncio.run(main())
