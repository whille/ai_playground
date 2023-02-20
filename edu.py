#!/usr/bin/env python

"""
use chatGPT to educate kids
I want to wrap chatGPT for kids education. python programming.
    input: voice to text.
    output: text, and voice.
"""

import speech_recognition as sr
import pyttsx3
from aip import AipSpeech
import toml

class Tutor:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = pyttsx3.init()
        cfg = toml.load('/etc/baidu.toml')['speech']
        # https://console.bce.baidu.com/ai/#/ai/speech/overview/index
        self.bd = AipSpeech(cfg['APP_ID'], cfg['APP_KEY'], cfg['SECRET_KEY'])

    def listen(self, sample_rate=16000):
        with sr.Microphone(sample_rate=sample_rate) as source:
            print("我在听|看...")
            audio = self.r.listen(source, phrase_time_limit=15)
            if not audio:
                return None
        try:
            return self.recognize(audio.frame_data, audio.sample_rate)
        except Exception as e:
            print(e)
            return None

    def watch(self):
        txt = input()
        return txt

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
        print(text)
        self.engine.say(text)
        self.engine.runAndWait()

    def loop(self, break_txt='Esc'):
        while True:
            text = self.listen()
            if text:
                response = "I heard you say: " + text
                if text.lower() == break_txt:
                    break
                self.speak(response)


if __name__ == '__main__':
    tutor = Tutor()
    tutor.loop()
