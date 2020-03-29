# From ID_VL.H / ID_VL.C
# Low-level video API

import ctypes

from sdl2 import *
import sdl2.ext

from palette import PALETTE

class VideoState():
    # TODO snake casing
    window = None
    renderer = None
    texture = None
    screen = None
    screenBuffer = None

    screenWidth = 640
    screenHeight = 400
    scaleFactor = 2

    cur_pitch = None
    cur_surface = None

state = VideoState()

def startup():
    # VL_SetVGAPlaneMode in ID_VL.C
    # initialize sdl video
    width, height = state.screenWidth, state.screenHeight

    state.window = SDL_CreateWindow(b'Wolfenstein 3D',
                                    SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                    width, height, SDL_WINDOW_ALLOW_HIGHDPI)
    state.renderer = SDL_CreateRenderer(state.window, -1, 0)
    state.texture = SDL_CreateTexture(state.renderer, SDL_PIXELFORMAT_ARGB8888,
                                SDL_TEXTUREACCESS_STREAMING, width, height)
    state.screen = SDL_CreateRGBSurface(0, width, height, 32, 0, 0, 0, 0)

    state.screenBuffer = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 8, 0, 0, 0, 0)
    sdlpal = SDL_AllocPalette(256);
    SDL_SetPaletteColors(sdlpal, PALETTE, 0, 256)
    SDL_SetSurfacePalette(state.screenBuffer, sdlpal);

    state.scaleFactor = min(width // 320, height // 200)

def flip():
    # http://sandervanderburg.blogspot.ro/2014/05/rendering-8-bit-palettized-surfaces-in.html
    pixels = ctypes.c_void_p()
    pitch = ctypes.c_int()
    SDL_LockTexture(state.texture, None, ctypes.byref(pixels), ctypes.byref(pitch))
    SDL_ConvertPixels(state.screen.contents.w,
                      state.screen.contents.h,
                      state.screen.contents.format.contents.format,
                      state.screen.contents.pixels,
                      state.screen.contents.pitch, SDL_PIXELFORMAT_ARGB8888,
                      pixels, pitch);

    SDL_UnlockTexture(state.texture)
    SDL_RenderCopy(state.renderer, state.texture, None, None)
    SDL_RenderPresent(state.renderer)



def lock_surface(surface):
    if SDL_MUSTLOCK(surface.contents):
        SDL_LockSurface(surface.contents)

    vbuf = ctypes.cast(surface.contents.pixels, ctypes.POINTER(ctypes.c_ubyte))
    return vbuf

def unlock_surface(surface):
    if SDL_MUSTLOCK(surface.contents):
        SDL_UnlockSurface(surface.contents)
