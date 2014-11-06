__all__ = ('Track', 'Clip')
 

class Track(object):
    app        = None
    clips      = []
    clip_class = None
    name       = None
    width      = None
    
    def __init__(self, name=None, clips=None, width=None):
        self.name   = name or self.name
        self.clips  = self.init_clips(clips or self.clips)
        self.width  = width or self.width

    def __setattr__(self, name, value):
        if name == 'app':
            for clip in self.clips:
                clip.app = value 
        super(Track, self).__setattr__(name, value)

    def init_clips(self, clips):
        return [self.make_clip(c) for c in clips]

    def make_clip(self, c):
        if self.clip_class is None \
        or isinstance(c, self.clip_class):
            return c
        clip = self.clip_class(c)
        clip.app = self.app
        return clip

    def add_clip(self, _):
        #self.widget.add.set_label('foo')
        clip = Clip('new_clip')
        self.clips.append(clip)
        #self.widget.clips.insert(-1, clip.get_widget())


class Clip(object):
    app  = None
    loop = True
    name = ''
    
    def __init__(self, name=None, loop=None):
        self.name = name or self.name
        self.loop = loop or self.loop

    def keypress(self, size, key):
        pass

    def launch(self, _):
        self.app.transport.enqueue(self.start)

    def stop(self):
        pass

    def start(self):
        pass

    def end(self):
        pass
