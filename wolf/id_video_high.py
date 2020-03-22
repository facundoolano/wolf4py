# From ID_VH.H / ID_VH.C
# High-level video API

from sdl2 import *
import id_video_low as vl

# TODO this could probably live in vl itself
def update_screen():
    vl.state.window.refresh()
    # SDL_BlitSurface(vl.state.screenBuffer, None, vl.state.screen, None);
    # vl.flip()
    # # ?
    # SDL_UpdateWindowSurface(vl.state.window)
