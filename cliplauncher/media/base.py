from ..events import Event


__all__ = ('Track', 'Clip')


class Clip(object):
    """ A clip represents a piece of media content.

        `Clip` is the base class for all such clips, and implements some
        common functionality which is shared among them. It can be named
        and optionally looped, as well as react to a number of relevant
        events, but does nothing on its own. In order to play a sound,
        look at `SooperLooperClip`.

        Subclasses of `Clip` implement concrete types of content which
        can be played back -- such as an audio sample or a MIDI sequence.
        Normally, playback is achieved by an external program -- such as
        SooperLooper or xjadeo. The clip object contains the data needed
        to control that program, such as the location of an audio sample
        and the rate at which it shall be played back, as well as a way
        to send such data to the program (e.g. via OSC).

        Clips are normally grouped in `Track`s. """

    ON_ADD      = Event()
    ON_EDIT     = Event()
    ON_REMOVE   = Event()
    ON_LAUNCH   = Event()
    ON_HALT     = Event()
    ON_START    = Event()
    ON_PROGRESS = Event()
    ON_END      = Event()

    loop = True
    name = ''
    
    def __init__(self, name=None, loop=None):
        self.name = name or self.name
        self.loop = loop or self.loop

    def launch(self, _):
        self.ON_LAUNCH(self)

    def halt(self):
        self.ON_HALT(self)

    def start(self):
        self.ON_START(self)

    def end(self):
        self.ON_END(self)

    def edit(self, values=None):
        if values:
            if 'name' in values:
                self.name = str(values['name'])
            if 'loop' in values:
                self.loop = bool(values['loop'])
        self.ON_EDIT(self, values)

    def get_fields(self):
        return (('name', 'Name', self.name),
                ('loop', 'Loop', self.loop))


class Track(object):
    """ A track is a container for clips.

        `Track` is the base class for all tracks. It implements common
        methods for handling a list of `Clip` objects, as well as a way
        for `Track` subclasses to initialize a list of clips from short
        representations -- e.g. a `XJadeoTrack` can populate itself with
        `XJadeoClips` based on a list of paths to video files.

        A `Track` can also contain things which are shared among all
        its clips -- such as an OSC connection to an external player
        program. Currently, when a clip is added to a track, a `track`
        attribute is set on the clip so that it can access attributes
        of the track. This means that a clip can't belong to multiple
        tracks simultaneously (or, more accurately, that it will only
        be able to see the last track to which it was added.) """

    ON_ADD    = Event()
    ON_REMOVE = Event()

    clip_class = None

    clips = []
    name  = None
    
    def __init__(self, name=None, clips=None):
        self.name  = name or self.name
        self.clips = self.init_clips(clips or self.clips)

    def init_clips(self, clips):
        return [self.init_clip(c) for c in clips]

    def init_clip(self, c):
        # do nothing if there's nothing to do
        # or you don't really know what to do
        if self.clip_class is None \
        or isinstance(c, self.clip_class):
            return c

        # since this base class isn't supposed to do
        # anything more complicated, but still needs
        # to handle strings somehow, strings are, by
        # default, used as names. subclass would put
        # something else here anyway.
        if isinstance(c, str):
            c = {'name': c}

        return self.new_clip(c)

    def new_clip(self, values):
        clip = self.clip_class(**values)
        self.add_clip(clip)
        return clip

    def add_clip(self, clip, pos=-1):
        self.clips.append(clip)
        clip.track = self
        Clip.ON_ADD(self, clip)

    def get_fields(self):
        return (('name', 'Name', ''),
                ('loop', 'Loop', True))
