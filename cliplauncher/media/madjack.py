import atexit
import liblo
from   subprocess import Popen, DEVNULL, PIPE
from   .base  import Track
from   .osc   import OSCClip
from   ..util import get_free_port


__all__ = ('MadJACKClip', 'MadJACKTrack')


class MadJACKClip(OSCClip):
    madjack = None

    def __init__(self, *a, **k):
        super(MadJACKClip, self).__init__(*a, **k)
        port = get_free_port()
        self.osc_address = liblo.Address(port)
        self.madjack = Popen(
            ['madjack', '-p', str(port), '-v',
                        '-l', 'system:playback_1',
                        '-r', 'system:playback_2',
                        self.name],
            stdin=PIPE, stderr=DEVNULL,
            stdout=open('/home/epimetheus/madjack'+str(port),'w'))
        atexit.register(lambda: self.kill())

    def build_message(self):
        return liblo.Message('/deck/play')

    def kill(self):
        liblo.send(self.osc_address, Message('/deck/stop'))
        self.madjack.kill()


class MadJACKTrack(Track):
    clip_class = MadJACKClip
