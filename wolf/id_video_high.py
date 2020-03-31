# From ID_VH.H / ID_VH.C
# High-level video API

from contextlib import contextmanager

from sdl2 import *
import id_video_low as id_vl
import id_cache as id_ca
import wl_def as de
import gfxv_wl6 as gfx

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


def draw_pic(chunknum):
    pic_bytes = id_ca.state.grsegs[chunknum]
    with lock_buffer() as surface:
        scaleFactor = id_vl.state.scaleFactor

        scy = 0
        for y in range(200):
            scx = 0
            for x in range(320):
                col = pic_bytes[(y * 80 + (x >> 2)) + (x & 3) * 80 * 200]
                for i in range(scaleFactor):
                    for j in range(scaleFactor):
                        surface[(scy + i) * surface.pitch + scx + j] = col

                scx += scaleFactor
            scy += scaleFactor


# FIXME this looks fairly simlar to draw surface above, reuse
def draw_pic_scaled_coord(destx, desty, chunknum):
    pic = id_ca.state.pictable[chunknum - gfx.STARTPICS]

    width, height = pic.width, pic.height
    source = id_ca.state.grsegs[chunknum]

    # FIXME copy paste
    with lock_buffer() as surface:
        scaleFactor = id_vl.state.scaleFactor

        scj = 0
        for y in range(height):
            sci = 0
            for x in range(width):
                col = source[(y * (width >> 2) + (x >> 2)) + (x & 3) * (width >> 2) * height]
                for i in range(scaleFactor):
                    for j in range(scaleFactor):
                        surface[(scj + i + desty) * surface.pitch + sci + j + destx] = col

                sci += scaleFactor
            scj += scaleFactor

@contextmanager
def lock_buffer():
    surface = id_vl.lock_surface(id_vl.state.screenBuffer)
    # this is a convenient hack, python won't let me yield a tuple
    surface.pitch = id_vl.state.screenBuffer.contents.pitch
    try:
        yield surface
    finally:
        id_vl.unlock_surface(id_vl.state.screenBuffer)

def update_screen():
    SDL_BlitSurface(id_vl.state.screenBuffer, None, id_vl.state.screen, None);
    id_vl.flip()
