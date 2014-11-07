from pdb        import post_mortem
from sys        import exc_info
from traceback  import print_exc
from urwid      import MainLoop, SelectEventLoop
from .transport import JACKOSCKlickTransport
from .ui.osc    import OscUI
from .ui.urwid  import UrwidUI


__all__ = ('ClipLauncher',)


class ClipLauncher(object):
    event_loop = None
    tracks     = []
    transport  = None

    def __init__(self, tracks=None, tempo=None):
        self.main_loop = MainLoop(widget=None)
        self.osc       = OscUI(self)
        self.transport = JACKOSCKlickTransport(tempo, osc=self.osc.server)
        self.tracks    = tracks or self.tracks
        self.urwid     = UrwidUI(self)

        self.main_loop.widget = self.urwid

    def start(self):
        try:
            self.main_loop.run()
        except:
            self.main_loop.stop()
            exc_type, value, tb = exc_info()
            print(
                "\nLooks like ClipLauncher has encountered an error :/" + 
                "\nHere's a chance to clean up and/or see what's going on.\n")
            print_exc()
            post_mortem(tb)
