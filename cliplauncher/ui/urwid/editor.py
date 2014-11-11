from urwid     import AttrMap, CheckBox, Columns, Edit, Frame, ListBox, \
                      Padding, SimpleFocusListWalker, Text, WidgetWrap
from ...media  import Clip, Track
from ...events import INFO


class EditorWidget(WidgetWrap):
    name  = None
    label = None
    value = None

    def __init__(self, name, label, value):
        self.name  = name
        self.label = label
        self.value = value
        self.widget = self.get_widget()

        WidgetWrap.__init__(self, Columns([
            ('weight', 1, Text(label, align='right')),
            ('weight', 3, self.widget)], 1))

    def get_widget(self):
        if isinstance(self.value, str):
            return AttrMap(Edit('', self.value), 'editable')
        elif isinstance(self.value, bool):
            return CheckBox('', self.value)
        else:
            return Text("Unknown field for {}".format(str(type(self.value))))

    def get_value(self):
        widget = self.widget.base_widget
        value  = None
        if isinstance(widget, Edit):
            value = widget.get_edit_text()
        elif isinstance(widget, CheckBox):
            value = widget.get_state()
        return (self.name, value)


class Editor(WidgetWrap):
    editing = None

    def __init__(self, track=None, clip=None):
        self.editing = clip or track

        self.header = Text('Editing clip {}'.format(clip.name)
             if  clip else 'Adding new clip to {}'.format(track.name)
             if track else 'Editor')
        self.widgets = [EditorWidget(name, label, default)
             for name, label, default
             in self.editing.get_fields()] \
             if self.editing else []
        self.body = ListBox(SimpleFocusListWalker(self.widgets))
        
        WidgetWrap.__init__(self, Frame(self.body, self.header))

    def rows(self, size, focus):
        return 10

    def keypress(self, size, key):
        if key == 'enter':
            values = dict([w.get_value() for w in self.widgets])
            if isinstance(self.editing, Clip):
                INFO(values)
        else:
            return super(Editor, self).keypress(size, key)


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

