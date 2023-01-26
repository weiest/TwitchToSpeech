import socket
import re
import random
import time

MAX_TIME_TO_WAIT_FOR_LOGIN = 3


class Twitch:
    re_prog = None
    sock = None
    partial = b''
    login_ok = False
    channel = ''
    login_timestamp = 0

    def __init__(self, channel):
        if self.sock:
            self.sock.close()
        self.sock = None
        self.partial = b''
        self.login_ok = False
        self.channel = channel
        self.re_prog = re.compile(
            b'^(?::(?:([^ !\r\n]+)![^ \r\n]*|[^ \r\n]*) )?([^ \r\n]+)(?: ([^:\r\n]*))?(?: :([^\r\n]*))?\r\n', re.MULTILINE)
        self.__twtich_connect__()

    def __twtich_connect__(self):
        print('[Twitch] Connecting to Twitch...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sock.connect(('irc.chat.twitch.tv', 6667))

        USER = 'justinfan%i' % random.randint(10000, 99999)
        PASSWORD = "asdf"
        login = "PASS {}\r\nNICK {}\r\n"
        print('[Twitch] Connected to Twitch. Logging in anonymously...')
        self.sock.send(login.format(PASSWORD, USER).encode())

        self.sock.settimeout(1.0/60.0)

        self.login_timestamp = time.time()

    def __reconnect__(self, delay):
        time.sleep(delay)
        self.__twtich_connect__()

    def __receive_and_parse_data__(self):
        buffer = b''
        while True:
            received = b''
            try:
                received = self.sock.recv(4096)
            except socket.timeout:
                break
            except Exception as e:
                print(
                    '[Twitch] Unexpected connection error. Reconnecting in a second...', e)
                self.__reconnect__(1)
                return []
            if not received:
                print(
                    '[Twitch] Connection closed by Twitch. Reconnecting in 5 seconds...')
                self.__reconnect__(5)
                return []
            buffer += received

        if buffer:
            if self.partial:
                buffer = self.partial + buffer
                self.partial = []

            res = []
            matches = list(self.re_prog.finditer(buffer))
            for match in matches:
                res.append({
                    'name':     (match.group(1) or b'').decode(errors='replace'),
                    'command':  (match.group(2) or b'').decode(errors='replace'),
                    'params':   list(map(lambda p: p.decode(errors='replace'), (match.group(3) or b'').split(b' '))),
                    'trailing': (match.group(4) or b'').decode(errors='replace'),
                })

            if not matches:
                self.partial += buffer
            else:
                end = matches[-1].end()
                if end < len(buffer):
                    self.partial = buffer[end:]

                if matches[0].start() != 0:
                    print(
                        '[Twitch] someone fucked up or twitch is bonkers, or both I mean who really knows anything at this point')

            return res

        return []

    def twitch_receive_messages(self):
        privmsgs = []
        for irc_message in self.__receive_and_parse_data__():
            cmd = irc_message['command']
            if cmd == 'PRIVMSG':
                privmsgs.append({
                    'username': irc_message['name'],
                    'message': irc_message['trailing'],
                    'time':  time.strftime("%H:%M:%S"),
                })
            elif cmd == 'PING':
                self.sock.send(b'PONG :tmi.twitch.tv\r\n')
            elif cmd == '001':
                print(
                    '[Twitch] Successfully logged in. Joining channel %s.' % self.channel)
                self.sock.send(('JOIN #%s\r\n' % self.channel).encode())
                self.login_ok = True
            elif cmd == 'JOIN':
                print('[Twitch] Successfully joined channel %s' %
                      irc_message['params'][0])
            elif cmd == 'NOTICE':
                print('[Twitch] Server notice:',
                      irc_message['params'], irc_message['trailing'])
            elif cmd == '002':
                continue
            elif cmd == '003':
                continue
            elif cmd == '004':
                continue
            elif cmd == '375':
                continue
            elif cmd == '372':
                continue
            elif cmd == '376':
                continue
            elif cmd == '353':
                continue
            elif cmd == '366':
                continue
            else:
                print('[Twitch] Unhandled irc message:', irc_message)

        if not self.login_ok:
            # We are still waiting for the initial login message. If we've waited longer than we should, try to reconnect.
            if time.time() - self.login_timestamp > MAX_TIME_TO_WAIT_FOR_LOGIN:
                print('[Twitch] No response from Twitch. Reconnecting...')
                self.reconnect(0)
                return []

        return privmsgs
