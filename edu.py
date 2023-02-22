#!/usr/bin/env python
import asyncio
import speech_recognition as sr
import pyttsx3
import platform
from chat import interact
from bd_voice import Baidu_Voice
from a_in import AInput


class Tutor:
    def __init__(self):
        self.r = sr.Recognizer()
        # usage: https://pypi.org/project/pyttsx3/
        self.engine = pyttsx3.init()
        if platform.machine == 'armv7l':
            self.engine.setProperty('voice', "Mandarin")
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
        if not text or text == '\n' or len(text) > 64:
            return
        print('speaking...')
        self.engine.say(text)
        self.engine.runAndWait()

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
        await self.bd.on_close()

    def show(self, gen):
        txt = ''
        cur_line = ''
        for w in gen:
            print(w, end='')
            cur_line += w
            if cur_line.endswith('\n'):
                self.speak(w)
                txt += cur_line
                cur_line = ''
        print('')
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
