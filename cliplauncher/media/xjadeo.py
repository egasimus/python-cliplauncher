import liblo
from   .base  import Track
from   .osc   import OSCClip
from   ..util import run, get_free_port


__all__ = ('XJadeoTrack', 'XJadeoClip')


class XJadeoClip(OSCClip):
    def __init__(self, *a, **k):
        super(XJadeoClip, self).__init__(*a, **k)
        self.path = self.name
        self.name = self.path.split('/')[-1]

    def build_message(self):
        return liblo.Bundle(
            liblo.Message('/jadeo/load', self.path),
            liblo.Message('/jadeo/seel', 0),
            liblo.Message('/jadeo/cmd'))


class XJadeoTrack(Track):
    clip_class = XJadeoClip
    osc_port   = None

    def __init__(self, *a, **k):
        self.osc_port     = k.get('port', self.osc_port) or get_free_port()
        self.osc_address  = liblo.Address(self.osc_port)
        super(XJadeoTrack, self).__init__(*a, **k)
        self.sooperlooper = run('xjadeo',
                                '-J',
                                '-O', str(self.osc_port))

    def init_clip(self, c):
        clip = super(XJadeoTrack, self).init_clip(c)
        clip.osc_address = self.osc_address
        return clip

