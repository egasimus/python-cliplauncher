from   enum       import Enum
import liblo
import mido
from   .util      import get_subprocess, get_free_port
    

class Transport(object):
    tempo = 140
    quant = None

    def __init__(self, tempo=None):
        self.tempo  = tempo or self.tempo

        jackosc_port = get_free_port()
        self._josc_address = liblo.Address(jackosc_port)
        self._josc  = get_subprocess('jack.osc', '-p', str(jackosc_port))
        self._klick = get_subprocess('klick', '-TP', str(self.tempo))
        self._jmclk = get_subprocess('jack_midi_clock')

    def play(self):
        liblo.send(self._josc_address, liblo.Message('/start'))

    def pause(self):
        liblo.send(self._josc_address, liblo.Message('/stop'))
