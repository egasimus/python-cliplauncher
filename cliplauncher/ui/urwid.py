from .base         import ClipLauncherUI
from ..events      import Event, INFO
from urwid         import (AttrMap, BoxAdapter, Button, Columns, ExitMainLoop,
                           Frame, Filler, ListBox, MainLoop, Pile,
                           SelectableIcon, SimpleFocusListWalker, Text,
                           WidgetWrap)
from urwid.signals import connect_signal


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


class BaseClipButton(Button):
    button_left  = None
    button_right = None

    def __init__(self, icon, label, on_press=None, user_data=None): 
        self._icon  = AttrMap(SelectableIcon(icon, 0), 'clip_empty')
        self._label = SelectableIcon(label, 0)

        cols = Columns([
            ('fixed', len(icon), self._icon),
            self._label],
            dividechars=1)
        WidgetWrap.__init__(self, cols)

        connect_signal(self, 'click', on_press, user_data)


class ClipButton(BaseClipButton):
    clip = None 

    def __init__(self, clip):
        self.clip = clip
        super(ClipButton, self).__init__('···', clip.name, self.on_click)

    def on_click(self, _):
        self._icon.base_widget.set_text('***')
        self.clip.launch(_)


class AddClipButton(BaseClipButton):
    def __init__(self, callback=None):
        super(AddClipButton, self).__init__(
            '+++', 'add clip', callback)


class TrackWidget(WidgetWrap):
    ON_ADD_CLIP = Event()

    track = None

    def __init__(self, track=None):
        self.track = track or self.track
        self.clips = SimpleFocusListWalker(
            [ClipButton(c) for c in self.track.clips] +
            [AddClipButton(self.on_add_clip)])
        self.header = Text('\n'+self.track.name+'\n')
        WidgetWrap.__init__(self, Frame(ListBox(self.clips),
                                        self.header))

    def on_add_clip(self, _):
        UrwidUI.add_clip(self)
        


class UrwidUI(WidgetWrap, ClipLauncherUI):

    palette = [('title',        'white',      'light gray'),
               ('header',       'white',      'light gray'),
               ('header_focus', 'white',      'dark red'),
               ('footer',       'white',      'black'),
               ('clip_focus',   'white',      'white'),
               ('clip_empty',   'light gray', 'white')]
    track_spacing = 2

    def __init__(self, app):
        ClipLauncherUI.__init__(self, app)

        # set colors
        self.app.main_loop.screen.register_palette(self.palette)

        # create widgets
        self.cols   = Columns(SimpleFocusListWalker(
            [TrackWidget(t) for t in self.app.tracks]),
            self.track_spacing)
        self.header = TransportWidget(app.transport)
        self.footer = AttrMap(Text('footer'), 'footer')
        self.editor = Text('editor')

        # listen to events
        INFO.append(self.on_info)

        WidgetWrap.__init__(self, Pile([
            ('pack', self.header),
            self.cols,
            ('pack', self.footer),
            ('pack', self.editor)]))

    def keypress(self, size, key):
        if key == 'q':
            raise ExitMainLoop
        return super(UrwidUI, self).keypress(size, key)

    def on_info(self, msg):
        self.footer.original_widget.set_text(str(msg))
        self._invalidate()
        self.app.main_loop.draw_screen()

    def add_clip(self, track, position=None):
        self.editor = None
