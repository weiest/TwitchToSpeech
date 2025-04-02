import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='main.log',level=logging.INFO)

from os import remove
from AudioEngine import AudioEngine
from VoiceEngine import VoiceEngine

audio = AudioEngine("CABLE Input (VB-Audio Virtual Cable)")
voice = VoiceEngine()
voice.setVoiceGender("Female")
voice.setPitch("1")
voice.setRate("60")

def command(message: str) -> None:
    arguments = message.split(" ")
    actions = {
        "help": lambda _: print(list(actions.keys())),
        "parameters": lambda _: print(voice.getParameters()),
        "language": lambda value: voice.setLanguage(value),
        "gender": lambda value: voice.setVoiceGender(value),
        "pitch":lambda value: voice.setPitch(float(value)),
        "rate":lambda value: voice.setRate(float(value)),
        "volume":lambda value: voice.setVolume(float(value)),
    }
    try:
        if len(arguments) == 1:
            actions[arguments[0]]("")
        else:
            actions[arguments[0]](arguments[1])
    except KeyError as e:
        logger.warning("Invalid Command")

message = "-"
while message != "":
    message = ""
    FILENAME = "speech.wav"
    message = input(f"[{voice.getLanguageName()}] Say: ")
    if message.startswith("/"):
        command(message[1:])
        continue
    try:
        voice.generateSpeech(message, FILENAME)
        audio.playAudio(FILENAME)
        remove(FILENAME)
    except Exception as e:
        logger.error(e)
        continue
