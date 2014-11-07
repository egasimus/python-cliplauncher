from ..events import Event


__all__ = ('Track', 'Clip')


class Clip(object):
    ON_ADD    = Event()
    ON_REMOVE = Event()
    ON_LAUNCH = Event()
    ON_STOP   = Event()
    ON_START  = Event()
    ON_END    = Event()

    loop = True
    name = ''
    
    def __init__(self, name=None, loop=None):
        self.name = name or self.name
        self.loop = loop or self.loop

    def launch(self, _):
        self.ON_LAUNCH(self)

    def stop(self):
        self.ON_STOP(self)

    def start(self):
        self.ON_START(self)

    def end(self):
        self.ON_END(self)
 

class Track(object):
    ON_ADD    = Event()
    ON_REMOVE = Event()

    clips      = []
    clip_class = None
    name       = None
    width      = None
    
    def __init__(self, name=None, clips=None, width=None):
        self.name   = name or self.name
        self.clips  = self.init_clips(clips or self.clips)
        self.width  = width or self.width

    def init_clips(self, clips):
        return [self.make_clip(c) for c in clips]

    def make_clip(self, c):
        if self.clip_class is None \
        or isinstance(c, self.clip_class):
            return c
        return self.clip_class(c)

    def add_clip(self, _):
        clip = Clip('new_clip')
        self.clips.append(clip)
        Clip.ON_ADD(clip)


#self.widget.add.set_label('foo')
#self.widget.clips.insert(-1, clip.get_widget())
