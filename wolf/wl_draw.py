import wl_def as de
import id_video_high as id_vh
import wl_game
import ctypes

from palette import PALETTE

def three_d_refresh():
    with id_vh.lock_buffer() as surface:
        clear_screen(surface)
        wall_refresh()
        draw_scaled_images()
        draw_player_weapon()

    id_vh.update_screen()

## internal functions

VGA_FLOOR_COLOR = 0x19
VGA_CEILING_COLORS = [
    0x1d,0x1d,0x1d,0x1d,0x1d,0x1d,0x1d,0x1d,0x1d,0xbf,
    0x4e,0x4e,0x4e,0x1d,0x8d,0x4e,0x1d,0x2d,0x1d,0x8d,
    0x1d,0x1d,0x1d,0x1d,0x1d,0x2d,0xdd,0x1d,0x1d,0x98,
    0x1d,0x9d,0x2d,0xdd,0xdd,0x9d,0x2d,0x4d,0x1d,0xdd,
    0x7d,0x1d,0x2d,0x2d,0xdd,0xd7,0x1d,0x1d,0x1d,0x2d,
    0x1d,0x1d,0x1d,0x1d,0xdd,0xdd,0x7d,0xdd,0xdd,0xdd
]

def clear_screen(vbuf):
    ceiling = VGA_CEILING_COLORS[wl_game.state.map_index]

    # write the upper half of the view with ceiling color
    width = id_vh.state.view_width
    height = id_vh.state.view_height
    ctypes.memset(vbuf, ceiling, width * height // 2)

    # move the pointer to the start of the floor and write the floor color
    floor_start = ctypes.cast(vbuf, ctypes.c_voidp).value + width * height // 2
    ctypes.memset(floor_start, VGA_FLOOR_COLOR, width * height // 2)

def wall_refresh():
    pass

def draw_scaled_images():
    pass

def draw_player_weapon():
    pass
