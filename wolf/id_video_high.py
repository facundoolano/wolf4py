# From ID_VH.H / ID_VH.C
# High-level video API

from sdl2 import *
import id_video_low as vl

# TODO this could probably live in vl itself
def update_screen():
    SDL_BlitSurface(vl.screenBuffer, None, vl.screen, None);
    vl.flip()
