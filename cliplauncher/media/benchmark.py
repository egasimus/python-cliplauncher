from .base import OSCClip, Track


__all__ = ('BenchmarkTrack', 'BenchmarkClip')


class BenchmarkClip(OSCClip):
    def start(self):
        pass


class BenchmarkTrack(Track):
    clip_class = BenchmarkClip
