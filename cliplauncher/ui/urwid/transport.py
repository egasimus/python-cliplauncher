from urwid import AttrMap, Columns, Button, Text, WidgetWrap


class BlockButton(Button):
    def __init__(self, label, on_press=None, user_data=None):
        Button.__init__(self, label, on_press, user_data)
        self._w = self._label


class TempoWidget(Button):
    transport = None

    def __init__(self, transport):
        self.transport = transport
        label = 'Tempo {0}BPM'.format(self.transport.tempo)
        Button.__init__(self, label)
        self._w = self._label


class MetronomeWidget(Button):
    transport = None
    click     = None

    def __init__(self, transport, click=False):
        self.transport = transport
        self.click     = click
        label = 'Click ON' if self.click else 'Click OFF'
        Button.__init__(self, label, self.on_click)
        self._w = self._label

    def on_click(self, _):
        self.click = not self.click
        if self.click:
            self.transport.click_on()
            self._w.set_text('Click ON')
        else:
            self.transport.click_off()
            self._w.set_text('Click OFF')


class PlayButton(BlockButton):
    transport = None
    playing   = False

    def __init__(self, transport, playing=False):
        self.transport = transport
        self.playing   = playing or self.playing
        BlockButton.__init__(self, '> PLAY', self.on_click)

    def on_click(self, _):
        self.playing = not self.playing
        if self.playing:
            self.transport.play() 
            self._label.set_text('|| PAUSE')
        else:
            self.transport.pause()
            self._label.set_text('> PLAY')


class RewindButton(BlockButton):
    transport = None
    can_rewind = False

    def __init__(self, transport, playing=False):
        self.transport = transport
        BlockButton.__init__(self, '|< REW', self.on_click)

    def on_click(self, _):
        self.transport.rewind()


class TransportWidget(WidgetWrap):
    transport = None

    def __init__(self, transport=None):
        self.transport = transport or self.transport
        WidgetWrap.__init__(self, AttrMap(Columns([
            ('weight', 1, PlayButton(self.transport)),
            ('weight', 1, RewindButton(self.transport)),
            ('weight', 3, Text('')),
            ('weight', 1, MetronomeWidget(self.transport)),
            ('weight', 1, TempoWidget(self.transport)),
            ('weight', 1, Text('Quant 1 bar')),
        ], 1), 'footer'))

