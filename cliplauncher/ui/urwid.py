from .     import ClipLauncherUI
from urwid import AttrMap, BoxAdapter, Button, Columns, ExitMainLoop, Frame, Filler, \
                  ListBox, MainLoop, SimpleFocusListWalker, Text, WidgetWrap


class DimButton(Button):
    button_left  = Text('+')
    button_right = Text('')


class ClipButton(Button):
    button_left  = AttrMap(Text('['), 'clip_empty')
    button_right = AttrMap(Text(']'), 'clip_empty')


class BlockButton(Button):
    def __init__(self, label, on_press=None, user_data=None):
        Button.__init__(self, label, on_press, user_data)
        self._w = self._label


class TempoButton(Button):
    transport = None

    def __init__(self, transport):
        self.transport = transport
        label = 'Tempo {0}BPM'.format(self.transport.tempo)
        Button.__init__(self, label)
        self._w = self._label


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
            self._w.set_text('|| PAUSE')
        else:
            self.transport.pause()
            self._w.set_text('> PLAY')


class TransportWidget(WidgetWrap):
    transport = None

    def __init__(self, transport=None):
        self.transport = transport or self.transport
        WidgetWrap.__init__(self, AttrMap(Columns([
            ('weight', 1, PlayButton(self.transport)),
            ('weight', 1, BlockButton('|< REW')),
            ('weight', 2, Text('')),
            ('weight', 1, TempoButton(self.transport)),
            ('weight', 1, Text('Quant 1 bar')),
        ], 1), 'footer'))


class TrackWidget(WidgetWrap):
    track = None

    def __init__(self, track=None):
        self.track = track or self.track
        self.add   = DimButton('', self.track.add_clip)
        self.clips = SimpleFocusListWalker(
            [self.get_clip_widget(c) for c in self.track.clips] +
            [AttrMap(self.add, 'clip_empty')])
        self.header = Text('\n'+self.track.name+'\n')
        WidgetWrap.__init__(self, Frame(ListBox(self.clips),
                                        self.header))

    def get_clip_widget(self, clip):
        return ClipButton(clip.name, clip.launch) if clip.name \
          else AttrMap(ClipButton(''), 'clip_empty')


class UrwidUI(WidgetWrap, ClipLauncherUI):
    palette = [('title',        'white',      'light gray'),
               ('header',       'white',      'light gray'),
               ('header_focus', 'white',      'dark red'),
               ('footer',       'white',      'black'),
               ('clip_focus',   'white',      'white'),
               ('clip_empty',   'light gray', 'white')]

    def __init__(self, app):
        ClipLauncherUI.__init__(self, app)

        self.app.main_loop.screen.register_palette(self.palette)

        self.cols   = Columns(SimpleFocusListWalker(
            [TrackWidget(t) for t in self.app.tracks]), 1)
        self.header = TransportWidget(app.transport)
        self.footer = AttrMap(Text('footer'), 'footer')

        WidgetWrap.__init__(self, Frame(
            self.cols, self.header, self.footer))

    def keypress(self, size, key):
        if key == 'q':
            raise ExitMainLoop
        return super(UrwidUI, self).keypress(size, key)

    def react(self, msg):
        self.footer.original_widget.set_text(str(msg))
        self._invalidate()
