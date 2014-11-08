from .editor    import EditorWidget
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
               ('clip_empty',   'light gray', 'white')]

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
        self.header = TransportWidget(app.transport)
        self.footer = AttrMap(Text('footer'), 'footer')
        self.editor = EditorWidget()

        # listen to events
        INFO.append(self.on_info)

        # init as pile of widgets
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
        self.editor.show()
        self._invalidate()
        self.app.main_loop.draw_screen()
