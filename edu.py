#!/usr/bin/env python
import asyncio
import speech_recognition as sr
from chat import interact
from bd_voice import Baidu_Voice
from a_in import AInput
from utils import logger
from speaker import play_audio_bytes

class Tutor:
    def __init__(self):
        self.r = sr.Recognizer()
        # usage: https://pypi.org/project/pyttsx3/
        self.bd = Baidu_Voice()
        self.aio = AInput()

    async def listen(self, sample_rate=16000):
        with sr.Microphone(sample_rate=sample_rate) as source:
            # self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source, phrase_time_limit=15)
            if not audio:
                return None
        try:
            # TODO use simple async.http
            return await self.bd.recognize(audio.get_wav_data())
        except Exception as e:
            print(e)
            return None

    # TODO Ctrl+C to stop
    def speak(self, text):
        if not text or text == '\n' or len(text) > 128:
            return
        print('speaking...')
        options = {
            'vol': 5,  # volume
        }
        # https://ai.baidu.com/ai-doc/SPEECH/Gk38y8lzk
        res = self.bd.speaker.synthesis(text, 'zh', 1, options)
        if not isinstance(res, dict):
            play_audio_bytes(res)
        else:
            logger.warning(res)

    async def loop(self, break_txt='\x1b'):    # Esc
        while True:
            text = await self.get_input()
            if not text:
                continue
            if text == break_txt or len(text) < 2:
                break
            print(f"I heard you say: {text}({len(text)})")
            try:
                self.show(interact(text, user=''))
            except Exception as e:
                print(f"e: {e}")

    def show(self, gen):
        txt = ''
        cur_line = ''
        for w in gen:
            print(w, end='')
            cur_line += w
            if cur_line.endswith('\n'):
                self.speak(cur_line)
                txt += cur_line
                cur_line = ''
        print('')
        self.speak(cur_line)
        return txt

    async def get_input(self):
        tasks = [self.text_input(), self.listen()]
        done, pending = await asyncio.wait(
            [asyncio.create_task(t) for t in tasks], return_when=asyncio.FIRST_COMPLETED)
        result = None
        for task in done:
            result = task.result()
        for task in pending:
            task.cancel()
        return result

    async def text_input(self):
        return await self.aio.input("waiting...(Esc)")

    async def voice_input(self):
        return await self.listen()


if __name__ == '__main__':
    tutor = Tutor()
    asyncio.run(tutor.loop())
