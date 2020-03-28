from sdl2 import *
import sdl2.ext


def user_input():
    # wait until user keypress
    # TODO alternatively delay?

    while True:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_KEYUP:
                return
