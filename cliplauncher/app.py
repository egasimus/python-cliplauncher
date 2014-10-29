from urwid      import MainLoop
from .transport import JACKTransport
from .ui.midi   import MidiUI
from .ui.urwid  import UrwidUI


__all__ = ('ClipLauncher',)


class ClipLauncher(object):
    tracks    = []
    transport = None
    ui        = {}

    def __init__(self, tracks=None):
        self.transport = JACKTransport()
        self.tracks = tracks or self.tracks
        self.ui.update({'urwid': UrwidUI(self),
                        'midi':  MidiUI(self)})
        self.main_loop = MainLoop(widget=self.ui['urwid'],
                                  palette=self.get_palette())

    def get_palette(self):
        return [('title',        'white',      'light gray'),
                ('header',       'white',      'light gray'),
                ('header_focus', 'white',      'dark red'),
                ('footer',       'white',      'dark cyan'),
                ('clip_focus',   'white',      'white'),
                ('clip_empty',   'light gray', 'white')]

    def start(self):
        self.main_loop.run()

    def react(self, msg):
        self.ui['urwid'].react(msg)
        self.main_loop.draw_screen()
