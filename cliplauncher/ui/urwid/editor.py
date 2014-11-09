from urwid import AttrMap, CheckBox, Columns, Edit, ListBox, Padding, \
                  SimpleFocusListWalker, Text, WidgetWrap


class EditorWidget(WidgetWrap):
    def __init__(self, track=None, clip=None):
        obj = clip or track
        WidgetWrap.__init__(self, ListBox(SimpleFocusListWalker(
            [self.get_field(f) for f in obj.get_editor_fields()])))

    def get_field(self, field):
        name, label, default = field
        if isinstance(default, str):
            return Edit(label + ' ', default)
        elif isinstance(default, bool):
            return CheckBox(label, default)
        else:
            return Text("Unknown field {}".format(label))

    def rows(self, size, focus):
        return 10


class EditorPanel(WidgetWrap):
    visible = False

    def __init__(self):
        WidgetWrap.__init__(self, self.wrap(ListBox([])))

    def wrap(self, w):
        return AttrMap(w, 'panel')

    def rows(self, size, focus):
        return 10 if self.visible else 0

    def show(self, track=None, clip=None):
        if track or clip:
            self._w = self.wrap(EditorWidget(track, clip))
        self.visible = True

    def hide(self):
        self.visible = False

