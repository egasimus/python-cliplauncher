from urwid import AttrMap, CheckBox, Columns, Edit, Frame, ListBox, \
                  Padding, SimpleFocusListWalker, Text, WidgetWrap


class EditorWidget(WidgetWrap):
    label = None
    value = None

    def __init__(self, label, value):
        self.label = label
        self.value = value

        WidgetWrap.__init__(self, Columns([
            Text(label),
            self.get_widget()],
        1))

    def get_widget(self):
        if isinstance(self.value, str):
            return AttrMap(Edit('', self.value), 'editable')
        elif isinstance(self.value, bool):
            return CheckBox('', self.value)
        else:
            return Text("Unknown field type {}".format(str(type(self.value))))


class Editor(WidgetWrap):
    editing = None

    def __init__(self, track=None, clip=None):
        self.editing = clip or track

        self.header = Text('Editing clip {}'.format(clip.name)
             if  clip else 'Adding new clip to {}'.format(track.name)
             if track else 'Editor')
        self.body = ListBox(SimpleFocusListWalker(
            [EditorWidget(label, default) for name, label, default
             in self.editing.get_fields()])
            if self.editing else [])
        
        WidgetWrap.__init__(self, Frame(self.body, self.header))

    def rows(self, size, focus):
        return 10


class Panel(WidgetWrap):
    visible = False

    def __init__(self):
        WidgetWrap.__init__(self, self.wrap(ListBox([])))

    def wrap(self, w):
        return AttrMap(w, 'panel')

    def rows(self, size, focus):
        return 10 if self.visible else 0

    def show(self, track=None, clip=None):
        if track or clip:
            self._w = self.wrap(Editor(track, clip))
        self.visible = True

    def hide(self):
        self.visible = False

