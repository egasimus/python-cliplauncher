import atexit
from   subprocess import Popen, DEVNULL


__all__ = ('run',)


def run(*args, **kwargs):
    stdin  = kwargs.get('stdin',  DEVNULL)
    stdout = kwargs.get('stdout', DEVNULL)
    stderr = kwargs.get('stderr', DEVNULL)
    subprocess = Popen(
        args, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
    atexit.register(lambda: subprocess.kill())
    return subprocess

