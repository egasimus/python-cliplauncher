from .     import ClipLauncherUI
from urwid import AttrMap, Button, Columns, ExitMainLoop, Frame, ListBox, \
                  MainLoop, SimpleFocusListWalker, Text, WidgetWrap


class DimButton(Button):
    button_left  = Text('+')
    button_right = Text('')


class ClipButton(Button):
    button_left  = AttrMap(Text('['), 'clip_empty')
    button_right = AttrMap(Text(']'), 'clip_empty')


class TrackWidget(WidgetWrap):
    track = None

    def __init__(self, track=None):
        self.track = track or self.track
        self.add   = DimButton('', self.track.add_clip)
        self.clips = SimpleFocusListWalker(
            [self.get_clip_widget(c) for c in self.track.clips] +
            [AttrMap(self.add, 'clip_empty')])
        self.header = Text(self.track.name)
        super(TrackWidget, self).__init__(Frame(ListBox(self.clips),
                                                self.header))

    def get_clip_widget(self, clip):
        return ClipButton(clip.name, clip.launch) if clip.name \
          else AttrMap(ClipButton(''), 'clip_empty')


class UrwidUI(WidgetWrap, ClipLauncherUI):

    def __init__(self, app):
        ClipLauncherUI.__init__(self, app)
        self.cols = Columns(SimpleFocusListWalker(
            [TrackWidget(t) for t in self.app.tracks]), 1)
        self.footer = AttrMap(Text('footer'), 'footer')
        WidgetWrap.__init__(self, Frame(self.cols, None, self.footer))

    def keypress(self, size, key):
        if key == 'q':
            raise ExitMainLoop
        return super(UrwidUI, self).keypress(size, key)

    def react(self, msg):
        self.footer.original_widget.set_text(str(msg))
        self._invalidate()
