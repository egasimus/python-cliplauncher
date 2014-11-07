import liblo
from urwid  import ExitMainLoop
from .base  import ClipLauncherUI
from ..util import get_free_port


class OscUI(ClipLauncherUI):
    def __init__(self, *a, **k):
        super(OscUI, self).__init__(*a, **k)
        
        self.port   = get_free_port()
        self.server = liblo.Server(self.port)
        #self.osc_server.add_method(None, None, self.on_osc)

        self.fd = self.server.fileno()
        self.app.main_loop.watch_file(self.fd, self.receive)

    def receive(self):
        while self.osc_server.recv(0): pass

    #def on_osc(self, path, args, types, src):
        #return
        #if path == '/tick':
            #self.app.react(args[0])
