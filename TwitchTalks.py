from AudioEngine import AudioEngine
from VoiceEngine import VoiceEngine
from Twitch import Twitch
import time
import concurrent.futures
import json
import re

# TODO: Change this to your needs
TWITCH_CHANNEL = ''
AUDIO_DEVICE = ''

FILENAME = 'speech.wav'
MESSAGE_RATE = 0.5
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100

audio = AudioEngine(AUDIO_DEVICE)
voice = VoiceEngine()
twitch = Twitch(TWITCH_CHANNEL)

last_time = time.time()
message_queue = []
thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)
active_tasks = []

PROFANITY_LIST = json.load(open("filter.json", "r"))
PROFANITY_REGEX = re.compile('|'.join(PROFANITY_LIST))


def filter_message(message):
    # Process message before playing it
    output = PROFANITY_REGEX.sub("", str(message))
    return output


def handle_message(message):
    user = message["username"]
    time = message["time"]
    msg = message["message"]
    msg = filter_message(message)
    print(f"[{time}] {user}: {msg}")
    try:
        voice.generateSpeech(msg, FILENAME)
        audio.playAudio(FILENAME)
    except:
        return


while True:
    active_tasks = [t for t in active_tasks if not t.done()]
    new_messages = twitch.twitch_receive_messages()
    if new_messages:
        message_queue += new_messages  # New messages are added to the back of the queue
        # Shorten the queue to only the most recent X messages
        message_queue = message_queue[-MAX_QUEUE_LENGTH:]
    messages_to_handle = []
    if not message_queue:
        last_time = time.time()
    else:
        r = 1 if MESSAGE_RATE == 0 else (
            time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time()
    if not messages_to_handle:
        continue
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(
                    thread_pool.submit(handle_message, message))
            else:
                print(
                    f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers ({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')
