#!/usr/bin/env python
import pyttsx3
import platform
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play


class Tts_speaker:

    def __init__(self):
        self.engine = pyttsx3.init()
        if platform.machine() == 'armv7l':
            self.engine.setProperty('voice', "zh")

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


def play_audio_bytes(mp3_bytes):
    audio_segment = AudioSegment.from_file(BytesIO(mp3_bytes), format="mp3")
    play(audio_segment)
