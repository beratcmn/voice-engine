# ------------------------- Imports -------------------------
# Voice Engine libraries
from gtts import gTTS
import speech_recognition as sr
import vlc
# General libraries
import time
from datetime import date
import os
import sys

# ------------------------- Global Variables -------------------------
r = sr.Recognizer()

today = date.today()
today = str(today).replace("-", " ")

nameCounter = 0

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()


# ------------------------- Functions -------------------------

def Talk(sentence):
    global nameCounter
    global vlc_instance
    global player
    nameCounter = nameCounter + 1
    fileName = "ses" + str(nameCounter) + ".wav"
    tts = gTTS(sentence, lang="tr", slow=False)
    tts.save(fileName)
    time.sleep(0.1)
    media = vlc_instance.media_new(fileName)
    player.set_media(media)
    player.play()
    time.sleep(0.5)
    duration = player.get_length()
    time.sleep(duration / 1000 - 0.5)
    player.stop()
    os.remove(fileName)


def Listen():
    with sr.Microphone() as source:
        print("Konuşabilirsiniz...")
        r.adjust_for_ambient_noise(source)
        try:
            voice = r.listen(source, timeout=2, phrase_time_limit=5)
            voice_data = r.recognize_google(voice, language="tr-tr")
            return voice_data
        except sr.WaitTimeoutError:
            Talk("Sizi dinlerken zaman aşımına uğradım.")
        except sr.UnknownValueError:
            Talk("Ne dediğinizi anlayamadım.")
        except sr.RequestError:
            print("İnternet bağlanırken bir hata oluştu. Lütfen tekrar deneyiniz.")
