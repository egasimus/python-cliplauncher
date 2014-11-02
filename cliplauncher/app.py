from urwid      import MainLoop, SelectEventLoop
from .transport import Transport
from .ui.midi   import MidiUI
from .ui.osc    import OscUI
from .ui.urwid  import UrwidUI


__all__ = ('ClipLauncher',)


class ClipLauncher(object):
    event_loop = None
    tracks     = []
    transport  = None
    ui         = {}

    def __init__(self, tracks=None):
        self.tracks = tracks or self.tracks
        for track in self.tracks:
            track.app = self

        self.main_loop = MainLoop(widget=None)

        self.ui.update({'osc':  OscUI(self),
                        'midi': MidiUI(self)})
        self.transport = Transport(self)

        self.ui.update({'urwid': UrwidUI(self)})
        self.main_loop.widget = self.ui['urwid']

    def start(self):
        self.main_loop.run()

    def react(self, event):
        for ui in self.ui.values():
            ui.react(event)

    def on_osc(self):
        msg = self.osc_server.recv()
