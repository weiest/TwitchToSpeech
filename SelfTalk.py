from AudioEngine import AudioEngine
from VoiceEngine import VoiceEngine
import json, re 

audio = AudioEngine()
voice = VoiceEngine()
voice.setFemaleVoice()
voice.setVolume(1)

PROFANITY_LIST = json.load(open("filter.json", "r"))
PROFANITY_REGEX = re.compile('|'.join(PROFANITY_LIST))

message = "-"
while (message != ''):
    FILENAME = 'speech.wav'
    message = input('Say>')
    message = PROFANITY_REGEX.sub("", str(message))
    try:
        voice.generateSpeech(message, FILENAME)
        audio.playAudio(FILENAME)
    except:
        continue
