import pyttsx3

class VoiceEngine:
    engine = None;

    def __init__(self):
        self.engine = pyttsx3.Engine()
    
    def __setVoiceGender__(self, voiceIndex: int):
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[voiceIndex].id)

    def setMaleVoice(self):
        self.__setVoiceGender__(0)

    def setFemaleVoice(self):
        self.__setVoiceGender__(1)

    def getVoiceGender(self) -> str:
        return self.engine.getProperty("voice")
    
    def setVolume(self, volume:float):
        self.engine.setProperty("volume", volume)

    def getVolume(self) -> float:
        return self.engine.getProperty("volume")
    
    def generateSpeech(self, message, filename):
        self.engine.save_to_file(message, filename)
        self.engine.runAndWait()