from urwid import AttrMap, Padding, Text, WidgetWrap


class EditorWidget(WidgetWrap):
    def __init__(self, track=None, clip=None):
        clip_or_track = clip or track
        fields = clip_or_track.get_editor_fields()
        WidgetWrap.__init__(self, Text(str(fields)))


class EditorPanel(WidgetWrap):
    visible = False

    def __init__(self):
        WidgetWrap.__init__(self, self.wrap(Text('Editor goes here.')))

    def wrap(self, w):
        return AttrMap(Padding(left=1, right=1, w=w), 'panel')

    def rows(self, size, focus):
        return 10 if self.visible else 0

    def show(self, track=None, clip=None):
        if track or clip:
            self._w = self.wrap(EditorWidget(track, clip))
        self.visible = True

    def hide(self):
        self.visible = False

