import liblo
from   .base  import Track
from   .osc   import OSCClip
from   ..util import run, get_free_port


__all__ = ('SooperLooperTrack', 'SooperLooperClip')


class SooperLooperClip(OSCClip):
    rate = 1.0

    def __init__(self, *a, **k):
        self.path = k.pop('path', '')
        self.name = k.pop('name', None) or self.path.split('/')[-1]
        self.rate = k.pop('rate', None) or self.rate
        super(SooperLooperClip, self).__init__(*a, **k)

    def build_message(self):
        return liblo.Bundle(
            liblo.Message('/sl/0/load_loop', self.path, '', ''),
            #liblo.Message('/sl/0/register_update/', 'scratch_pos', '', ''),
            liblo.Message('/sl/0/hit', 'trigger'))

    def get_fields(self):
        return (('name', 'Name', self.name),
                ('path', 'Path', self.path),
                ('loop', 'Loop', self.loop),
                ('rate', 'Rate', self.rate))

    def edit(self, values):
        super(SooperLooperClip, self).edit(values)


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

    def init_clip(self, c):
        if isinstance(c, str):
            c = {'path': c}
        clip = super(SooperLooperTrack, self).init_clip(c)
        clip.osc_address = self.osc_address
        return clip

    def get_fields(self):
        return (('name', 'Name', ''),
                ('path', 'Path', ''),
                ('loop', 'Loop', True),
                ('rate', 'Rate', 1.0))
