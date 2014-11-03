from .base import Clip, Track
import liblo


class OSCClip(Clip):
    osc_address = None

    def start(self, _):
        liblo.send(self.osc_address, self.build_message())

    def build_message(self):
        return liblo.Message('/ping')


class OSCTrack(Track):
    clip = OSCClip
