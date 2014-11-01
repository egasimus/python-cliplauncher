import mido
from .     import ClipLauncherUI


mido.set_backend('mido.backends.rtmidi')


class MidiUI(ClipLauncherUI):
    port_in  = None
    port_out = None    

    def __init__(self, app):
        ClipLauncherUI.__init__(self, app)
        self.port_in = mido.open_input(mido.get_input_names()[0],
                                       callback=self.on_msg)

    def on_msg(self, msg):
        self.app.on_event(msg)
