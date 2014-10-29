import atexit
from   subprocess import Popen, DEVNULL
from   .base  import Clip, Track


class MPlayerClip(Clip):
    mplayer = None

    def __init__(self, *a, **k):
        super(MPlayerClip, self).__init__(*a, **k)
        self.mplayer = Popen(['mplayer', '-loop', '0', '-slave', self.name],
                             stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL)
        atexit.register(lambda: self.mplayer.kill())


class MPlayerTrack(Track):
    clip_class = MPlayerClip
