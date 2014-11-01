from urwid      import MainLoop
from .transport import Transport
from .ui.midi   import MidiUI
from .ui.urwid  import UrwidUI


__all__ = ('ClipLauncher',)


class ClipLauncher(object):
    tracks    = []
    transport = None
    ui        = {}

    def __init__(self, tracks=None):
        self.transport = Transport()
        self.tracks = tracks or self.tracks
        self.main_loop = MainLoop(widget=None)
        self.ui.update({'urwid': UrwidUI(self),
                        'midi':  MidiUI(self)})
        self.main_loop.widget = self.ui['urwid']

    def start(self):
        self.main_loop.run()

    def on_event(self, event):
        self.ui['urwid'].react(event)
        self.main_loop.draw_screen()
