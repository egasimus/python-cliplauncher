from .base import Clip, Track
import liblo


class OSCClip(Clip):
    osc_address = None

    def start(self):
        liblo.send(self.osc_address, self.build_message())
        super(OSCClip, self).start()

    def build_message(self):
        return liblo.Message('/ping')


class OSCTrack(Track):
    clip = OSCClip
