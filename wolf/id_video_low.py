# From ID_VL.H / ID_VL.C
# Low-level video API
from sdl2 import *
import sdl2
import sdl2.ext
import ctypes
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

# initialize sdl video
# TODO rename?
def set_vga_plane_mode():
    width, height = state.screenWidth, state.screenHeight

    # state.window = sdl2.ext.Window("Pixel Access", size=(width, height), flags=SDL_WINDOW_ALLOW_HIGHDPI)
    # state.window.show()
    state.window = SDL_CreateWindow(b'Wolfenstein 3D',
                                    SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED,
                                    width, height, SDL_WINDOW_ALLOW_HIGHDPI)
    state.renderer = SDL_CreateRenderer(state.window, -1, 0)
    state.texture = SDL_CreateTexture(state.renderer, SDL_PIXELFORMAT_ARGB8888,
                                SDL_TEXTUREACCESS_STREAMING, width, height)
    state.screen = SDL_CreateRGBSurface(0, width, height, 32, 0, 0, 0, 0)

    # FIXME load palette?
    # ?
    # memcpy(curpal, gamepal, sizeof(SDL_Color) * 256);

    # FIXME 32 works, 8 not
    # If depth is 4 or 8 bits, an empty palette is allocated for the surface. If depth is greater than 8 bits, the pixel format is set using the [RGBA]mask parameters.
    state.screenBuffer = SDL_CreateRGBSurface(SDL_SWSURFACE, width, height, 32, 0, 0, 0, 0);


    # SDL_Palette *sdlpal = SDL_AllocPalette(256);
    # SDL_SetPaletteColors(sdlpal, gamepal, 0, 256);

    # screenPitch = screen->pitch;
    # bufferPitch = screenBuffer->pitch;

    # state.cur_surface = state.screenBuffer
    # state.cur_pitch = state.screenBuffer.contents.pitch

    state.scaleFactor = min(width // 320, height // 200)

    # pixelangle = (short *) malloc(screenWidth * sizeof(short));
    # CHECKMALLOCRESULT(pixelangle);
    # wallheight = (int *) malloc(screenWidth * sizeof(int));
    # CHECKMALLOCRESULT(wallheight);

# http://sandervanderburg.blogspot.ro/2014/05/rendering-8-bit-palettized-surfaces-in.html
def flip():
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

def draw_surface(pic_bytes):
    # surface = state.window.get_surface()
    # sdl2.ext.fill(surface, sdl2.ext.Color(0,0,0))
    surface = state.screenBuffer.contents
    pixelview = sdl2.ext.pixels2d(surface)

    scy = 0
    for y in range(200):
        scx = 0
        for x in range(320):
            col = pic_bytes[(y * 80 + (x >> 2)) + (x & 3) * 80 * 200]
            for i in range(state.scaleFactor):
                for j in range(state.scaleFactor):
                    # vbuf[(scy + i) * state.cur_pitch + scx + j] = col
                    pixelview[scx + j][scy + i] = PALETTE[col]

            scx += state.scaleFactor
        scy += state.scaleFactor

    del pixelview
