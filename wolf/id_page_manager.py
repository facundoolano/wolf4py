import ctypes
from util import datafile, readctype
from io import BytesIO

class PageState():
    textures = []
    sprites = []
    sounds = []

class CompShape(ctypes.Structure):
    # table data after dataofs[right_pix-left_pix+1]
    _fields_ = [('left_pix', ctypes.c_ushort),
                ('right_pix', ctypes.c_ushort),
                ('dataofs', ctypes.c_ushort * 64)]

state = PageState()

def startup():
    with datafile('VSWAP') as handle:
        _, chunks_in_file = readctype(handle, ctypes.c_ushort)
        _, pm_sprite_start = readctype(handle, ctypes.c_ushort)
        _, pm_sound_start = readctype(handle, ctypes.c_ushort)

        t_page_offsets = ctypes.c_uint32 * (chunks_in_file + 1)
        _, page_offsets = readctype(handle, t_page_offsets)

        t_page_lengths = ctypes.c_ushort * chunks_in_file
        _, page_lengths = readctype(handle, t_page_lengths)

        # load textures, sprites and sounds into memory
        # all fit in memory so we skip the paging mechanism
        for i in range(chunks_in_file):
            if not page_offsets[i]:
                # sparse page
                continue

            # Use specified page length, when next page is sparse page.
            # Otherwise, calculate size from the offset difference between this and the next page.
            size = page_offsets[i + 1] - page_offsets[i]
            if not page_offsets[i + 1]:
                size = page_lengths[i]

            handle.seek(page_offsets[i])

            value = handle.read(size)
            if i < pm_sprite_start:
                state.textures.append(value)
            elif i < pm_sound_start:
                # for sprites we parse the CompShape struct as well
                bio = BytesIO(value)
                comp_shape = CompShape()
                bio.readinto(comp_shape)
                state.sprites.append((comp_shape, value))
            else:
                value = handle.read(size)
                state.sounds.append(value)

def get_sprite(shape_num):
    return state.sprites[shape_num]
