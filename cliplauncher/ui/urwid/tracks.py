from urwid import AttrMap, BoxAdapter, Button, Columns, Filler, Frame, \
                  ListBox, SelectableIcon, SimpleFocusListWalker, WidgetWrap
from urwid.signals import connect_signal
from ...events     import INFO
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
    def __init__(self, ui, clip):
        self.clip = clip
        self.ui   = ui
        Clip.ON_EDIT.append(self.on_edit)
        Clip.ON_START.append(self.on_start)
        Clip.ON_PROGRESS.append(self.ui.on_info)
        super(ClipButton, self).__init__('···', clip.name, self.on_click)

    def set_icon(self, icon):
        self._icon.base_widget.set_text(icon)

    def on_click(self, _):
        self.set_icon('***')
        self.clip.launch(_)

    def on_edit(self, clip, values):
       if clip == self.clip:
            if 'name' in values:
                self._label.set_text(values['name'])

    def on_start(self, clip):
        if clip == self.clip:
            self.set_icon('-->')

    def keypress(self, size, key):
        if key == 'ctrl e':
            self.ui.editor.show(clip=self.clip)
        return super(ClipButton, self).keypress(size, key)


class AddClipButton(BaseClipButton):
    def __init__(self, callback=None):
        super(AddClipButton, self).__init__(
            '+++', 'add clip', callback)


class TrackWidget(WidgetWrap):
    number = None
    track  = None
    ui     = None

    def __init__(self, ui=None, track=None, number=None):
        self.ui     = ui     or self.ui
        self.track  = track  or self.track
        self.number = number or self.number
 
        self.header = TrackHeader(self.track.name, number)
        self.clips = SimpleFocusListWalker(
            [ClipButton(self.ui, c) for c in self.track.clips] +
            [AddClipButton(self.on_add_button)])

        Clip.ON_ADD.append(self.on_clip_added)

        WidgetWrap.__init__(self, Frame(ListBox(self.clips),
                                        header=self.header))

    def on_add_button(self, _):
        self.ui.editor.show(track=self.track)

    def on_clip_added(self, track, clip):
        if track == self.track:
            self.clips.insert(-1, ClipButton(self.ui, clip))
