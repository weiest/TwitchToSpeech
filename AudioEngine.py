from pygame import mixer, _sdl2 as audiodevices
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'


class AudioEngine:
    def __initMixer__(self, name) -> bool:
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

    def __init__(self, device=""):
        self.initialized = False
        print(f"[Audio] Initializing Audio Interface")
        if (device != ""):
            if (self.__initMixer__(device)):
                print(f"[Audio] Successfully Initialized using {device}")
                return
            else:
                print(f"[Audio] Failed to Initialize using {device}")
        print(f"[Audio] Attempting to use Audio Devices from System")
        for device in self.__getListOfDevices__():
            attempt = ""
            while (attempt not in ["y", "n"]):
                attempt = input("[Audio] Use "+device+"? (Y/N):")
                attempt = attempt.lower()
            if (attempt == "n"):
                continue
            if (self.__initMixer__(device)):
                print(f"[Audio] Successfully Initialized using {device}")
                break
            else:
                print(f"[Audio] Failed to Initialize using {device}")
                print(f"[Audio] Skipping..")
                continue
        if not self.initialized:
            print(f"[Audio] No Audio Device has been selected, quitting.")
            quit()

    def playAudio(self, filename) -> bool:
        try:
            channel = mixer.find_channel()
            channel.play(mixer.Sound(filename))
            return True
        except:
            return False
