import sys
import ctypes
import time

from sdl2 import *
import sdl2.ext

import id_cache as id_ca
import id_video_high as id_vh
import id_video_low as id_vl
import id_input as id_in
import wl_game
import gfxv_wl6 as gfx

# TODO add import sort, pep8 and whatnot

def main():
    init_game()
    demo_loop()

    quit_()
    return 0

def init_game():
    sdl2.ext.init()
    id_vl.startup()

    id_ca.startup()

# TODO rename, there's no demo here
def demo_loop():
    id_ca.cache_screen(gfx.TITLEPIC)
    id_vh.update_screen()

    id_in.user_input()

    wl_game.loop()

def quit_():
    SDL_DestroyWindow(id_vl.state.window)
    SDL_Quit()


if __name__ == "__main__":
    sys.exit(main())
