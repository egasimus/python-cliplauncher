__all__ = ('Track', 'Clip')
 

class Track(object):
    clips      = []
    clip_class = None
    name       = None
    width      = None
    
    def __init__(self, name=None, clips=None, width=None):
        self.name   = name or self.name
        self.clips  = self.init_clips(clips or self.clips)
        self.width  = width or self.width

    def init_clips(self, clips):
        return [self.get_clip(c) for c in clips]

    def get_clip(self, clip):
        if self.clip_class:
            return self.clip_class(clip)
        else:
            return clip

    def add_clip(self, _):
        #self.widget.add.set_label('foo')
        clip = Clip('new_clip')
        self.clips.append(clip)
        #self.widget.clips.insert(-1, clip.get_widget())


class Clip(object):
    name = None
    
    def __init__(self, name=None):
        self.name = name or ''

    def keypress(self, size, key):
        pass

    def launch(self, _):
        pass


