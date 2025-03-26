import logging
logger = logging.getLogger(__name__)
import pyttsx3
from typing import NoReturn
from enum import Enum

class Gender(Enum):
    MALE = 0
    FEMALE = 1

class Language(Enum):
    ENGLISH = 409
    JAPANESE = 411

class VoiceEngine:
    def __init__(self) -> NoReturn:
        self.engine = pyttsx3.Engine()
        self.language = Language.ENGLISH

    def setVoiceGender(self, gender: str) -> NoReturn:
        gender = gender.upper()
        if gender in Gender.__members__:
            voices = self.engine.getProperty('voices')
            self.engine.setProperty('voice', voices[Gender[gender].value].id)
        else:
            logger.warning(f"{gender} is not a valid option")
    def getVoiceGender(self) -> str:
        return self.engine.getProperty("voice")

    def setVolume(self, volume: float) -> NoReturn:
        self.engine.setProperty("volume", volume)
    def getVolume(self) -> float:
        return self.engine.getProperty("volume")

    def setRate(self, rate:float) -> NoReturn:
        self.engine.setProperty("rate", rate)
    def getRate(self) -> float:
        return self.engine.getProperty("rate")

    def setPitch(self, pitch:float) -> NoReturn:
        self.pitch = pitch
    def getPitch(self) -> float:
        if hasattr(self, 'pitch'):
            return self.pitch
        return None

    def setLanguage(self, language: str) -> NoReturn:
        language = language.upper()
        if language in Language.__members__:
            self.language = Language[language]
        else:
            logger.warning(f"{language} is not a valid option")
    def getLanguageName(self) -> str:
        return self.language.name
    def getLanguageValue(self) -> str:
        return self.language.value

    def generateSpeech(self, message: str, filename: str) -> NoReturn:
        if self.getPitch():
            message = f"<pitch middle='{self.getPitch()}'>{message}</pitch>"
        message = f"<lang langid='{self.getLanguageValue()}'>{message}</lang>"
        self.engine.save_to_file(message, filename)
        self.engine.runAndWait()
