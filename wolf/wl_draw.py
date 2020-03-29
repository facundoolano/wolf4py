import wl_def as de
from wl_def import Sprites
import id_video_high as id_vh
import wl_game
import id_page_manager as id_pm
import ctypes
from util import read_word, read_short


from palette import PALETTE

def three_d_refresh():
    with id_vh.lock_buffer() as surface:
        clear_screen(surface)
        wall_refresh()
        draw_scaled_images()
        draw_player_weapon(surface)

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

WEAPON_SCALE = [Sprites.KNIFEREADY, Sprites.PISTOLREADY,
                Sprites.MACHINEGUNREADY, Sprites.CHAINREADY]

def draw_player_weapon(vbuf):
    shapenum = WEAPON_SCALE[wl_game.state.weapon].value + wl_game.state.weaponframe
    simple_scale_shape(vbuf, shapenum)

# TODO used only once and seems similar to scale_shape, see if they can be
# unified
def simple_scale_shape(vbuf, shape_num):
    view_width, view_height = id_vh.state.view_width, id_vh.state.view_height
    xcenter = view_width // 2
    height = view_height + 1

    shape, shape_bytes = id_pm.get_sprite(shape_num)

    scale = height >> 1
    pixheight = scale * de.SPRITE_SCALE_FACTOR
    actx = xcenter - scale
    upperedge = view_height // 2 - scale

    # cmdptr=(word *) shape->dataofs;
    cmdptr = iter(shape.dataofs)

    # import pdb; pdb.set_trace()
    i = shape.left_pix
    pixcnt = i * pixheight
    rpix = (pixcnt >> 6) + actx

    # for(i=shape->leftpix,pixcnt=i*pixheight,rpix=(pixcnt>>6)+actx;i<=shape->rightpix;i++,cmdptr++)
    while i <= shape.right_pix:
        lpix = rpix
        if lpix >= view_width:
            break

        pixcnt += pixheight
        rpix = (pixcnt >> 6) + actx

        if lpix != rpix and rpix > 0:

            if lpix < 0:
                lpix = 0
            if rpix > view_width:
                rpix = view_width
                i = shape.right_pix + 1

            # cline points to the offset indicated by the next cmdptr item
            # cline=(byte *)shape + *cmdptr;
            cline = shape_bytes[next(cmdptr):]
            while lpix < rpix:
                # turn into bytearray to pop when moving the pointer
                # maybe better to iterate some other way
                line = bytearray(cline)
                endy = read_word(line, byteorder='little')
                while endy:
                    endy >>= 1
                    newstart = read_short(line, byteorder='little')
                    starty = read_word(line, byteorder='little') >> 1;
                    j = starty
                    ycnt = j * pixheight
                    screndy = (ycnt >> 6) + upperedge

                    if screndy < 0:
                        vmem_index = lpix
                    else:
                        vmem_index = screndy * vbuf.pitch + lpix

                    while j < endy:
                        scrstarty = screndy
                        ycnt += pixheight
                        screndy = (ycnt >> 6) + upperedge
                        if scrstarty != screndy and screndy > 0:
                            col = shape_bytes[newstart+j]
                            if scrstarty < 0:
                                scrstarty = 0
                            if screndy > view_height:
                                screndy = view_height
                                j = endy

                            while scrstarty < screndy:
                                vbuf[vmem_index] = col
                                vmem_index += vbuf.pitch
                                scrstarty += 1
                        j += 1

                    endy = read_word(line, byteorder='little')
                lpix += 1
        i += 1


class CompShape(ctypes.Structure):
    # table data after dataofs[right_pix-left_pix+1]
    _fields_ = [('left_pix', ctypes.c_ushort),
                ('right_pix', ctypes.c_ushort),
                ('dataofs', ctypes.c_ushort * 64)]
