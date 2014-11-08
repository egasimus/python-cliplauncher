from urwid import Padding, Text, WidgetWrap


class EditorWidget(WidgetWrap):
    visible = False

    def __init__(self):
        WidgetWrap.__init__(self,
            Padding(left=1, right=1, w=Text('Editor goes here.')))

    def rows(self, size, focus):
        return 10 if self.visible else 0

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False

