# TwitchToSpeech
TwitchToSpeech is script where it gives your twitch chat a "voice".

## How does it work?
There are 3 main modules each responsible to doing their thing.
 - `AudioEngine.py` is responsible for playing the sounds (using *pygame*)
 - `VoiceEngine.py` is responsible for generating the speech files (using *pyttsx3*)
 - `Twitch.py` is responsible for the connecting to Twitch (Thanks [DougDoug](https://github.com/DougDougGithub/TwitchPlays))

`SelfTalk.py` will allow you to "play around" and test the script without Twitch while `TwitchTalks.py` is the main script.

## How to Use?
### Install
This requires pyttsx3 and pygame (and their Prerequisite), more information can be found in `requirements.txt`
```
pip install -r requirements.txt
```

### Usage
Within TwitchTalks.py, locate the following two lines and specify the right parameters will do.
```
TWITCH_CHANNEL = ''
AUDIO_DEVICE = ''
```
If the AudioEngine can't find the device, it will prompt and iterate through a list of devices available on your system.  