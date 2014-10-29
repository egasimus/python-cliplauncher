#!/usr/bin/env python3


import curses


class Clip(object):
    name = ""

    def __init__(self, name):
        self.name = name


class Track(object):
    name  = ""
    clips = []
    view  = None

    def __init__(self, name, clips=None):
        self.name = name
        self.clips = clips or [Clip("")]

    def render(self, column, width):
        name_width = width - len(str(column)) - 2
        track_name = self.name.rjust(name_width)[:name_width]
        track_name_and_number = '{0} {1}'.format(column+1, track_name)
        header_style = curses.A_REVERSE if column == self.view.active_track \
                  else curses.A_NORMAL
        self.view.screen.addnstr(0, column*width, track_name_and_number,
                            width - 1, header_style)

        # Render each clip in this track
        for j, clip in enumerate(range(10)):
            is_active = column == self.view.active_track and j == self.view.active_clip
            clip_style = curses.A_REVERSE if is_active else curses.A_NORMAL
            self.view.screen.addstr(j+1, column*width, '.'*(width-1),
                               curses.color_pair(1) | clip_style)
            #self.screen.addch(j+1, i*track_width, curses.ACS_VLINE)
        


class SessionView(object):
    screen        = None
    width, height = None, None
    tracks        = []
    active_track  = 0
    active_clip   = 0

    def __init__(self, screen, tracks=None):
        self.screen = screen
        self.tracks = tracks or []
        for t in tracks:
            t.view = self
        self.height, self.width = screen.getmaxyx()
        self.init_colors()
        curses.curs_set(0)
        self.main_loop()

    def init_colors(self):
        curses.use_default_colors()
        for n, f, b in ((1, curses.COLOR_WHITE, curses.COLOR_BLACK),
                        (2, curses.COLOR_RED,   curses.COLOR_BLACK)):
            curses.init_pair(n, f, b)

    def main_loop(self):
        while True:
            self.render()
            key = self.screen.getkey()
            if self.handle_key(key):
                break

    def handle_key(self, key):
        if key == 'q':
            return True

        if key == 'KEY_LEFT':
            self.active_track = max(0,
                                    self.active_track - 1)
        if key == 'KEY_RIGHT':
            self.active_track = min(len(self.tracks) - 1,
                                    self.active_track + 1)

    def render(self):
        # Render each track
        track_width = int(self.width / len(self.tracks))
        for i, track in enumerate(self.tracks):
            track.render(i, track_width)

        # Render status ba


def get_tracks():
    T, C = Track, Clip
    return [T("Overtone"), T("Tidal"), T("Samples"), T("Sequencer"), T("Scenes")]


curses.wrapper(SessionView, get_tracks())
