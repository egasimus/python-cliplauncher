import liblo
from   .base  import Track
from   .osc   import OSCClip
from   ..util import run, get_free_port


__all__ = ('SooperLooperTrack', 'SooperLooperClip')


class SooperLooperClip(OSCClip):
    def __init__(self, *a, **k):
        super(SooperLooperClip, self).__init__(*a, **k)
        self.path = self.name
        self.name = self.path.split('/')[-1]

    def build_message(self):
        return liblo.Bundle(
            liblo.Message('/sl/0/load_loop', self.path, '', ''),
            liblo.Message('/sl/0/hit', 'trigger'))


class SooperLooperTrack(Track):
    clip_class = SooperLooperClip
    discrete   = False
    osc_port   = None

    def __init__(self, *a, **k):
        self.osc_port     = k.get('port', self.osc_port) or get_free_port()
        self.osc_address  = liblo.Address(self.osc_port)
        self.discrete     = k.get('discrete', self.discrete)
        super(SooperLooperTrack, self).__init__(*a, **k)
        self.sooperlooper = run('sooperlooper',
                                '-j', str(self.name),
                                '-l', '1',
                                '-p', str(self.osc_port),
                                '-D', 'yes' if self.discrete else 'no')
        liblo.send(self.osc_address, '/set', 'sync_source', -1)
        

    def make_clip(self, c):
        clip = super(SooperLooperTrack, self).make_clip(c)
        clip.osc_address = self.osc_address
        return clip
