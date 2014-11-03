import atexit
import socket
from   subprocess import Popen, DEVNULL


def get_free_port():
    s = socket.socket()
    s.bind(("", 0))
    return s.getsockname()[1]


def run(*args, **kwargs):
    stdin  = kwargs.get('stdin',  DEVNULL)
    stdout = kwargs.get('stdout', DEVNULL)
    stderr = kwargs.get('stderr', DEVNULL)
    subprocess = Popen(
        args, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
    atexit.register(lambda: subprocess.kill())
    return subprocess
