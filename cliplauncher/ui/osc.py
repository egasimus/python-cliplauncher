import liblo
from urwid   import ExitMainLoop
from .base   import ClipLauncherUI
from ..util  import get_free_port


class OscUI(ClipLauncherUI):
    def __init__(self, *a, **k):
        super(OscUI, self).__init__(*a, **k)
        self.port   = get_free_port()
        self.server = liblo.Server(self.port)
        self.fd     = self.server.fileno()
        self.app.main_loop.watch_file(self.fd, self.receive)

    def receive(self):
        while self.server.recv(0): pass
