# From ID_VH.H / ID_VH.C
# High-level video API

from contextlib import contextmanager

from sdl2 import *
import id_video_low as id_vl
import wl_def as de

class VideoState():
    view_size = 20
    view_width = -1
    view_height = -1

state = VideoState()

def new_view_size():
    # originally in wl_main.c
    # we only care about view size 20 (visible status but no other frame)
    set_view_size(id_vl.state.screenWidth,
                  id_vl.state.screenHeight - id_vl.state.scaleFactor * de.STATUS_LINES)

def set_view_size(width, height):
    # originally in wl_main.c
    state.view_width = width&~15                  # must be divisable by 16
    state.view_height = height&~1                 # must be even
    # centerx = id_vl.state.view_width // 2 - 1
    # shootdelta = id_vl.state.view_width // 10

    #calculate trace angles and projection constants
    #CalcProjection (FOCALLENGTH);


def draw_surface(pic_bytes):
    with lock_buffer() as surface:
        pitch = id_vl.state.screenBuffer.contents.pitch
        scaleFactor = id_vl.state.scaleFactor

        scy = 0
        for y in range(200):
            scx = 0
            for x in range(320):
                col = pic_bytes[(y * 80 + (x >> 2)) + (x & 3) * 80 * 200]
                for i in range(scaleFactor):
                    for j in range(scaleFactor):
                        surface[(scy + i) * pitch + scx + j] = col

                scx += scaleFactor
            scy += scaleFactor


@contextmanager
def lock_buffer():
    surface = id_vl.lock_surface(id_vl.state.screenBuffer)

    try:
        yield surface
    finally:
        id_vl.unlock_surface(id_vl.state.screenBuffer)

def update_screen():
    SDL_BlitSurface(id_vl.state.screenBuffer, None, id_vl.state.screen, None);
    id_vl.flip()
