# From ID_VH.H / ID_VH.C
# High-level video API

from sdl2 import *
import id_video_low as vl

def update_screen():
    # TODO this should probably live in vl itself
    SDL_BlitSurface(vl.state.screenBuffer, None, vl.state.screen, None);
    vl.flip()
