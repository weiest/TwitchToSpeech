import logging
logger = logging.getLogger(__name__)
from os import environ
from typing import NoReturn
from pygame import mixer, _sdl2 as audiodevices
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

class AudioEngine:
    def __initMixer__(self, name:str) -> bool:
        try:
            mixer.init(devicename=name)
            self.initialized = True
            return True
        except:
            return False

    def __getListOfDevices__(self) -> list:
        mixer.init()
        devices = audiodevices.audio.get_audio_device_names(False)
        mixer.quit()
        return devices

    def __init__(self, device:str=None) -> NoReturn:
        self.initialized = False
        logger.info(f"[Audio] Initializing Audio Interface")
        if (device):
            if (self.__initMixer__(device)):
                logger.info(f"[Audio] Successfully Initialized using {device}")
                return
            else:
                logger.warning(f"[Audio] Failed to Initialize using {device}")
        logger.info(f"[Audio] Attempting to use Audio Devices found from System with User Input required!")
        for device in self.__getListOfDevices__():
            attempt = ""
            while (attempt not in ["y", "n"]):
                attempt = input("[Audio] Use "+device+"? (Y/N):")
                attempt = attempt.lower()
            if (attempt == "n"):
                continue
            if (self.__initMixer__(device)):
                logger.info(f"[Audio] Successfully Initialized using {device}")
                break
            else:
                logger.warning(f"[Audio] Failed to Initialize using {device}")
                logger.warning(f"[Audio] Skipping..")
                continue
        if not self.initialized:
            logger.error(f"[Audio] No Audio Device has been selected, quitting.")
            raise RuntimeError("No Audio Device selected, unable to proceed")

    def playAudio(self, filename: str) -> bool:
        try:
            channel = mixer.find_channel()
            channel.play(mixer.Sound(filename))
            return True
        except:
            return False
