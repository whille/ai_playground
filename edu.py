#!/usr/bin/env python
import asyncio
import speech_recognition as sr
import pyttsx3
from aip import AipSpeech
import toml
import platform
from chat import interact

class Tutor:
    def __init__(self):
        self.r = sr.Recognizer()
        # usage: https://pypi.org/project/pyttsx3/
        self.engine = pyttsx3.init()
        if platform.machine == 'armv7l':
            self.engine.setProperty('voice', "Mandarin")
        cfg = toml.load('/etc/baidu.toml')['speech']
        # https://console.bce.baidu.com/ai/#/ai/speech/overview/index
        self.bd = AipSpeech(cfg['APP_ID'], cfg['APP_KEY'], cfg['SECRET_KEY'])

    def listen(self, sample_rate=16000):
        with sr.Microphone(sample_rate=sample_rate) as source:
            audio = self.r.listen(source, phrase_time_limit=15)
            if not audio:
                return None
        try:
            return self.recognize(audio.frame_data, audio.sample_rate)
        except Exception as e:
            print(e)
            return None

    def recognize(self, audio_data, rate, dev_pid=1536):
        # dev_pid列表:  https://ai.baidu.com/ai-doc/SPEECH/Vk38lxily
        result = self.bd.asr(audio_data, 'wav', rate, {
            'dev_pid': dev_pid,
        })
        if result['err_no'] == 0:
            return result['result'][0]
        else:
            raise Exception(result['err_msg'])

    def speak(self, text):
        if not text:
            return
        print("start speak...")
        self.engine.say(text)
        self.engine.runAndWait()

    async def loop(self, break_txt='\x1b'):    # Esc
        while True:
            text = await self.get_input()
            if not text:
                continue
            if text == break_txt or len(text) < 2:
                break
            print(f"I heard you say: {text}, {len(text)}")
            try:
                response = self.show(interact(text, user=''))
                self.speak(response)
            except Exception as e:
                print(f"e: {e}")

    def show(self, gen):
        txt = ''
        for w in gen:
            print(w, end='')
            txt += w
        print('')
        return txt

    async def get_input(self):
        tasks = [self.text_input(), self.voice_input()]
        done, pending = await asyncio.wait([asyncio.create_task(t) for t in tasks], return_when=asyncio.FIRST_COMPLETED)
        result = None
        for task in done:
            # print(f'{task} completed')
            result = task.result()
        for task in pending:
            task.cancel()
        return result

    async def text_input(self):
        text = await asyncio.to_thread(input, "waiting...(Esc)")
        return text

    async def voice_input(self):
        text = await asyncio.to_thread(self.listen)
        return text


if __name__ == '__main__':
    tutor = Tutor()
    asyncio.run(tutor.loop())
