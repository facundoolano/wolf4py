import sys
import ctypes
import time

from sdl2 import *
import sdl2.ext

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

    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
        # id_vh.update_screen()

    return 0

def init_game():
    sdl2.ext.init()
    id_vl.set_vga_plane_mode()

    id_ca.startup()

def demo_loop():
    id_ca.cache_screen(gfx.TITLEPIC)
    id_vh.update_screen()

    # TODO should wait for input instead

def quit_():
    SDL_DestroyWindow(id_vl.state.window)

    SDL_Quit()


if __name__ == "__main__":
    sys.exit(main())
