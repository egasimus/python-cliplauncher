from .editor    import Panel
from .tracks    import TrackWidget
from .transport import TransportWidget
from ..base     import ClipLauncherUI
from ...events  import INFO
from urwid      import AttrMap, Columns, ExitMainLoop, Pile, \
                       SimpleFocusListWalker, Text, WidgetWrap


class UrwidUI(WidgetWrap, ClipLauncherUI):

    palette = [('title',        'white',      'light gray'),
               ('header',       'white',      'light gray'),
               ('header_focus', 'white',      'dark red'),
               ('footer',       'white',      'black'),
               ('clip_focus',   'white',      'white'),
               ('clip_dim',     'light gray', 'white'),
               ('editable',     'yellow',     'black'),
               ('panel',        'white',      'light gray')]

    track_spacing = 2

    def __init__(self, app):
        ClipLauncherUI.__init__(self, app)

        # set colors
        self.app.main_loop.screen.register_palette(self.palette)

        # create widgets
        tracks = enumerate(self.app.tracks)
        self.cols   = Columns(SimpleFocusListWalker(
            [TrackWidget(self, t, n + 1) for n, t in tracks]),
            self.track_spacing)
        self.editor = Panel()
        self.header = TransportWidget(app.transport)
        self.footer = AttrMap(Text('foo'), 'footer')

        # listen to events
        INFO.append(self.on_info)

        # init as pile of widgets
        WidgetWrap.__init__(self, Pile([
            ('pack', self.header),
            self.cols,
            (10, self.editor),
            ('pack', self.footer)]))

    def on_info(self, msg):
        self.footer.original_widget.set_text(str(msg))
        self._invalidate()
        self.app.main_loop.draw_screen()

    def keypress(self, size, key):
        if key == 'ctrl w':
            raise ExitMainLoop
        return super(UrwidUI, self).keypress(size, key)
