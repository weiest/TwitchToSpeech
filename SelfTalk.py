from AudioEngine import AudioEngine
from VoiceEngine import VoiceEngine

audio = AudioEngine()
voice = VoiceEngine()
voice.setFemaleVoice()
voice.setVolume(1)

message = "-"
while (message != ""):
    FILENAME = "speech.wav"
    message = input("Say>")
    try:
        voice.generateSpeech(message, FILENAME)
        audio.playAudio(FILENAME)
    except:
        continue
