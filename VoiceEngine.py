import logging
logger = logging.getLogger(__name__)
import pyttsx3
from enum import Enum

class Gender(Enum):
    MALE = 0
    FEMALE = 1

class Language(Enum):
    ENGLISH = 409
    JAPANESE = 411

class VoiceEngine:
    def __init__(self) -> None:
        self.engine = pyttsx3.init() # pyttsx3.Engine()
        self.language = Language.ENGLISH

    def setVoiceGender(self, gender: str) -> None:
        gender = gender.upper()
        if gender in Gender.__members__:
            voices = self.engine.getProperty('voices')
            self.voiceGender = Gender[gender]
            self.engine.setProperty('voice', voices[self.voiceGender.value].id)
        else:
            logger.warning(f"{gender} is not a valid option")
    def getVoiceGenderName(self) -> str:
        return self.voiceGender.name
    def getVoiceGenderValue(self) -> str:
        return self.voiceGender.value

    def setVolume(self, volume: float) -> None:
        self.engine.setProperty("volume", volume)
    def getVolume(self) -> float:
        return self.engine.getProperty("volume")

    def setRate(self, rate:float) -> None:
        self.engine.setProperty("rate", rate)
    def getRate(self) -> float:
        return self.engine.getProperty("rate")

    def setPitch(self, pitch:int) -> None:
        self.pitch = pitch
    def getPitch(self) -> int:
        if hasattr(self, 'pitch'):
            return int(self.pitch)
        return None
    
    def setLanguage(self, language: str) -> None:
        language = language.upper()
        if language in Language.__members__:
            self.language = Language[language]
        else:
            logger.warning(f"{language} is not a valid option")
    def getLanguageName(self) -> str:
        return self.language.name
    def getLanguageValue(self) -> str:
        return self.language.value    

    def getParameters(self) -> str:
        return {
            "language": self.getLanguageName(),
            "gender": self.getVoiceGender(),
            "pitch": self.getPitch(),
            "rate": self.getRate(),
            "volume": self.getVolume(),
        }

    def sayMessage(self, message:str) -> None:
        self.engine.say(message)
        self.engine.runAndWait()
            
    def generateSpeech(self, message: str, filename: str) -> None:
        if not message:
            return
        if self.getPitch():
            message = f"<pitch middle='{self.getPitch()}'>{message}</pitch>"
        message = f"<lang langid='{self.getLanguageValue()}'>{message}</lang>"
        self.engine.save_to_file(message, filename)
        self.engine.runAndWait()

if __name__ == "__main__":
    voice = VoiceEngine()
    voice.sayMessage('The quick brown fox jumped over the lazy dog')
