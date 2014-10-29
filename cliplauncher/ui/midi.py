import mido
from .     import ClipLauncherUI


class MidiUI(ClipLauncherUI):
    port_in  = None
    port_out = None    

    def __init__(self, app):
        ClipLauncherUI.__init__(self, app)
        self.port_in = mido.open_input(mido.get_input_names()[0],
                                       callback=self.on_message)

    def on_message(self, msg):
        self.app.react(msg)
