# From ID_VH.H / ID_VH.C
# High-level video API

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

def update_screen():
    # TODO this should probably live in vl itself
    SDL_BlitSurface(id_vl.state.screenBuffer, None, id_vl.state.screen, None);
    id_vl.flip()
