"""
 arecord -l
 arecord -d 5 test.wav
 https://www.labno3.com/2021/08/09/using-a-microphone-with-a-raspberry-pi/
"""
import speech_recognition as sr

r = sr.Recognizer()
with sr.Microphone(sample_rate=16000) as source:
    # self.r.adjust_for_ambient_noise(source)
    audio = r.listen(source, phrase_time_limit=15)
