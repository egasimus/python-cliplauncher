from .base import Clip, Track
import liblo


class OSCClip(Clip):
    def start(self):
        liblo.send(self.track.osc_address, self.build_message())
        super(OSCClip, self).start()

    def build_message(self):
        return liblo.Message('/ping')


class OSCTrack(Track):
    clip = OSCClip
