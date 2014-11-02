from   enum       import Enum
import liblo
import math
import mido
from   .util      import run, get_free_port


class Transport(object):
    quant = None
    tempo = 140
    time  = 0

    def __init__(self, app, tempo=None):
        self.app   = app
        self.osc   = self.app.ui['osc'].osc_server
        self.tempo = tempo or self.tempo

        # jack.osc controls the jack transport
        jackosc_port           = get_free_port()
        self._jack_osc_address = liblo.Address(jackosc_port)
        self._jack_osc         = run('jack.osc', '-p', str(jackosc_port))

        # klick is jack tempo master
        klick_port          = get_free_port()
        self._klick_address = liblo.Address(klick_port)
        self._klick         = run('klick', '-T',
                                           # '-o', str(jackosc_port), TODO
                                           '-P', '-v', '0',
                                           str(self.tempo))

        # listen to jack.osc's timing messages
        self.osc.send(self._jack_osc_address, '/receive', 0xfffffff)
        self.osc.add_method('/pulse',     None, self.on_osc_pulse)
        self.osc.add_method('/tick',      None, self.on_osc_tick)
        self.osc.add_method('/drift',     None, self.on_osc_drift)
        self.osc.add_method('/transport', None, self.on_osc_transport)

    def on_osc_pulse(self, path, args):
        return
        self.app.react('pulse {} {} {} {} {} {} {}'.format(*args))

    def on_osc_tick(self, path, args):
        pulse = args[4]
        new_time = pulse % 1
        if new_time < self.time:
            self.on_beat(math.trunc(pulse))
        self.time = new_time

    def on_osc_drift(self, path, args):
        return
        self.app.react('drift')

    def on_osc_transport(self, path, args):
        return
        self.app.react('transport')

    def on_beat(self, beat):
        self.app.react('tick: pulse {0}'.format(beat))

    def play(self):
        liblo.send(self._jack_osc_address, liblo.Message('/start'))

    def pause(self):
        liblo.send(self._jack_osc_address, liblo.Message('/stop'))
