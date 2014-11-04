from   enum       import Enum
import liblo
import math
import mido
import sys
from   .util      import run, get_free_port


class At(tuple):
    def __new__(cls, bar=None, beat=None, time=None):
        return super(At, cls).__new__(cls, (bar, beat, time))

    def __init__(self, bar=None, beat=None, time=None):
        super(At, self).__init__()
        self.bar  = bar
        self.beat = beat
        self.time = time


class Meter(tuple):
    def __new__(cls, upper, lower):
        return super(Meter, cls).__new__(cls, (upper, lower))

    def __init__(self, upper, lower):
        super(Meter, self).__init__()
        self.upper = upper
        self.lower = lower

    def __str__(self):
        return "{}/{}".format(self.upper, self.lower)


class Transport(object):
    quant   = None
    tempo   = 140.0
    meter   = Meter(4, 4) 

    rolling = False
    bar     = 0
    beat    = 0
    time    = 0

    queue   = {}

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
        self._klick         = run('klick', '-T', '-P', '-v', '1.0',
                                           str(self.meter), str(self.tempo))

        # listen to jack.osc's timing messages
        self.osc.send(self._jack_osc_address, '/receive', 0xfffffff)
        self.osc.add_method('/pulse',     None, self.on_osc_pulse)
        self.osc.add_method('/tick',      None, self.on_osc_tick)
        self.osc.add_method('/drift',     None, self.on_osc_drift)
        self.osc.add_method('/transport', None, self.on_osc_transport)

        # rewind transport to start
        self.rewind()

    def on_osc_pulse(self, path, args):
        ntp, utc, frm, pntp, putc, pfrm, pulse = args
        return
        self.app.react('pulse {} {} {} {} {} {} {}'.format(*args))

    def on_osc_tick(self, path, args):
        if not self.rolling:
            return
        ntp, utc, frm, frame, pulse = args
        new_time = pulse % 1
        if new_time < self.time:
            self.on_beat(math.trunc(pulse))
        self.time = new_time

    def on_osc_drift(self, path, args):
        ntp, utc, frm, ntpdif, utcdif = args

    def on_osc_transport(self, path, args):
        ntp, utc, frm, fps, ppm, ppc, pt, state = args
        self.app.react('transport {}'.format(args))
        self.tempo
        if self.meter != (ppc, pt):
            self.meter = Meter(ppc, pt)
        self.rolling = state == 1

    def on_beat(self, beat):
        self.app.react('{}.{} {}'.format(self.bar, self.beat, self.meter))

        self.beat += 1
        if self.beat >= self.meter.upper:
            self.beat = 0
            self.bar += 1
        time = At(self.bar, self.beat, 0)
        for callback in self.queue.get(time, []):
            self.app.react('callback {} at {}'.format(callback, time))
            callback()

    def get_next_quant(self):
        return At(self.bar + 2, 0, 0)

    def enqueue(self, callback, time=None):
        time   = time or self.get_next_quant()
        events = self.queue.get(time, [])
        events.append(callback)
        self.queue.update({time: events})
        self.app.react('enqueue {} at {}'.format(callback, time))

    def play(self):
        liblo.send(self._jack_osc_address, '/start')

    def pause(self):
        liblo.send(self._jack_osc_address, '/stop')

    def rewind(self):
        self.osc.send(self._jack_osc_address, '/stop')
        self.osc.send(self._jack_osc_address, '/locate', 0)
        self.bar, self.beat, self.time = 0, 0, 0

    def click_on(self):
        liblo.send(self._klick_address, '/klick/config/set_volume', 1.0)

    def click_off(self):
        liblo.send(self._klick_address, '/klick/config/set_volume', 0.0)
