import sys
import ctypes
import time

from sdl2 import *

import id_cache as id_ca
import id_video_high as id_vh
import id_video_low as id_vl
import gfxv_wl6 as gfx

# TODO add import sort, pep8 and whatnot

def main():
    init_game()

    # TODO remove sdl hello world stuff

    demo_loop()

    # SDL_BlitSurface(image, None, windowsurface, None)
    # SDL_UpdateWindowSurface(window)

    quit_()

    return 0

def init_game():
    SDL_Init(SDL_INIT_VIDEO)
    id_vl.set_vga_plane_mode()

    id_ca.startup()

def demo_loop():
    id_ca.cache_screen(gfx.TITLEPIC)
    id_vh.update_screen()

    # TODO should wait for input instead
    time.sleep(20)

def quit_():
    SDL_DestroyWindow(id_vl.window)

    SDL_Quit()


if __name__ == "__main__":
    sys.exit(main())
