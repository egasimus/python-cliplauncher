from urwid import AttrMap, BoxAdapter, Button, Columns, Filler, Frame, \
                  ListBox, SelectableIcon, SimpleFocusListWalker, WidgetWrap
from urwid.signals import connect_signal
from ...media.base import Clip


class BaseClipButton(Button):
    button_left  = None
    button_right = None

    def __init__(self, icon, label, on_press=None, user_data=None): 
        self._icon  = AttrMap(SelectableIcon(icon, 0), 'clip_dim')
        self._label = SelectableIcon(label, 0)

        cols = Columns([
            ('fixed', len(icon), self._icon),
            self._label],
            dividechars=1)
        WidgetWrap.__init__(self, cols)

        connect_signal(self, 'click', on_press, user_data)


class TrackHeader(WidgetWrap):
    def __init__(self, name, number):
        WidgetWrap.__init__(self, BoxAdapter(Filler(BaseClipButton(
            str(number).rjust(3), name), top=1, bottom=1), height=3))


class ClipButton(BaseClipButton):
    clip = None 

    def __init__(self, clip):
        self.clip = clip
        Clip.ON_START.append(self.on_start)
        super(ClipButton, self).__init__('···', clip.name, self.on_click)

    def set_icon(self, icon):
        self._icon.base_widget.set_text(icon)

    def on_click(self, _):
        self.set_icon('***')
        self.clip.launch(_)

    def on_start(self, clip):
        if clip == self.clip:
            self.set_icon('-->')


class AddClipButton(BaseClipButton):
    def __init__(self, callback=None):
        super(AddClipButton, self).__init__(
            '+++', 'add clip', callback)


class TrackWidget(WidgetWrap):
    number = None
    track  = None
    ui     = None

    def __init__(self, ui=None, track=None, number=None):
        self.ui     = ui or self.ui
        self.track  = track or self.track
        self.number = number or self.number
 
        self.clips = SimpleFocusListWalker(
            [ClipButton(c) for c in self.track.clips] +
            [AddClipButton(self.on_add_clip)])
        self.header = TrackHeader(self.track.name, number)

        WidgetWrap.__init__(self, Frame(ListBox(self.clips),
                                        self.header))

    def on_add_clip(self, _):
        self.ui.add_clip(self)

