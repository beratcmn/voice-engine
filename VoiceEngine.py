# ------------------------- Imports -------------------------
# Voice Engine libraries
from gtts import gTTS
import speech_recognition as sr
import vlc
# General libraries
import time
import os

# ------------------------- Global Variables -------------------------
r = sr.Recognizer()

vlc_instance = vlc.Instance()
player = vlc_instance.media_player_new()

nameCounter = 0

wakeSentence = "Arif"

inConversation = False

# ------------------------- Functions -------------------------


def Talk(sentence):
    global nameCounter
    global vlc_instance
    global player
    nameCounter = nameCounter + 1
    fileName = "ses" + str(nameCounter) + ".wav"
    try:
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
    except Exception as e:
        print(e)


def Listen():
    global inConversation
    global wakeSentence
    global vlc_instance
    global player

    if inConversation == False:
        with sr.Microphone() as source:
            print("Bekleme modundayım ve sizi dinliyorum...")
            r.adjust_for_ambient_noise(source)
            try:
                voice = r.listen(source, timeout=7, phrase_time_limit=4)
                voice_data = r.recognize_google(voice, language="tr-tr")
                print(voice_data)
                if wakeSentence in voice_data:
                    inConversation = True
                    Talk("Efendim")
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except sr.RequestError as e:
                print(e)
    else:
        media = vlc_instance.media_new("beep.mp3")
        player.set_media(media)
        player.play()
        time.sleep(0.5)
        duration = player.get_length()
        time.sleep(duration/1000 - 0.5)
        player.stop()
        time.sleep(0.05)

        with sr.Microphone() as source:
            print("Konuşabilirsiniz...")
            r.adjust_for_ambient_noise(source)
            try:
                voice = r.listen(source, timeout=10, phrase_time_limit=10)
                voice_data = r.recognize_google(voice, language="tr-tr")
                print("Siz: " + str(voice_data))
                return voice_data
            except:
                inConversation = False


# ------------------------- Program -------------------------
