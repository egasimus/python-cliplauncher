import atexit
from   mplayer    import Player, CmdPrefix, PIPE
from   subprocess import Popen, DEVNULL
from   .base      import Clip, Track


__all__ = ('MPlayerClip', 'MPlayerTrack')


class MPlayerClip(Clip):
    player = None
    loop   = True

    def __init__(self, *a, **k):
        self.loop = k.pop('loop', self.loop)
        super(MPlayerClip, self).__init__(*a, **k)
        args = ('-ao', 'jack')
        self.player = Player(args, DEVNULL, DEVNULL)
        self.player.loadfile(self.name)
        if self.loop:
            self.player.loop = 0

    def launch(self, _):
        self.player.pause()


class MPlayerTrack(Track):
    clip_class = MPlayerClip
