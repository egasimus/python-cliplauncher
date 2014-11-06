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

        #liblo.send(self.app.transport.jack_osc_port, '/connect',
                   #self.name+':common_out_1', 'system:playback_1')
        #liblo.send(self.app.transport.jack_osc_port, '/connect',
                   #self.name+':common_out_2', 'system:playback_2')
        #run('jack_connect', self.name+':common_out_1', 'system:playback_1')
        #run('jack_connect', self.name+':common_out_2', 'system:playback_2')
        liblo.send(self.osc_address, '/set', 'sync_source', -1)
        liblo.send(self.osc_address, '/set', 'quantize', 2)

    def __setattr__(self, name, value):
        if name == 'app':
            liblo.send(value.transport._jack_osc_address, '/connect',
                       self.name+':common_out_1', 'system:playback_1')
            liblo.send(value.transport._jack_osc_address, '/connect',
                       self.name+':common_out_2', 'system:playback_2')
        super(SooperLooperTrack, self).__setattr__(name, value)
        

    def make_clip(self, c):
        clip = super(SooperLooperTrack, self).make_clip(c)
        clip.osc_address = self.osc_address
        return clip
