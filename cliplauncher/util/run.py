import atexit
from   subprocess import Popen, DEVNULL


__all__ = ('run',)


def run(*args, **kwargs):
    stdin  = kwargs.get('stdin',  DEVNULL)
    stdout = kwargs.get('stdout', DEVNULL)
    stderr = kwargs.get('stderr', DEVNULL)
    subprocess = Popen(
        args, stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)

    def kill():
        print('killing {} "{}" ...'.format(subprocess.pid, ' '.join(args)))
        subprocess.kill()

    atexit.register(kill)

    return subprocess
