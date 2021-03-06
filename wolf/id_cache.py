# From ID_CA.H / ID_CA.CPP
# Loads and decompresses asset files and makes the available at RAM.
import id_video_low as vl
import gfxv_wl6 as gfx
import ctypes
from io import BytesIO

import wl_def as de
from util import datafile, readctype, read_word, write_word

NUM_MAPS = 60
MAP_PLANES = 2

class HuffNode(ctypes.Structure):
    _fields_ = [('bit0', ctypes.c_ushort),
                ('bit1', ctypes.c_ushort)]

class MapHeader(ctypes.Structure):
    _fields_ = [('plane_start', ctypes.c_int32 * 3),
                ('plane_length', ctypes.c_ushort * 3),
                ('width', ctypes.c_ushort),
                ('height', ctypes.c_ushort),
                ('name', ctypes.c_char * 16)]

class Picture(ctypes.Structure):
    _fields_ = [('width', ctypes.c_int16),
                ('height', ctypes.c_int16)]

# TODO change names to more readable ones (and keep the others for reference)
class CacheState():
    # graphics
    grhuffman = []
    pictable = []
    grsegs = []

    # map
    RLEWtag = None
    maphandle = datafile('GAMEMAPS')
    mapheaderseg = []
    mapsegs = []

state = CacheState()

def startup():
    setup_map_file()
    setup_graphics_file()
    setup_audio_file()

def shutdown():
    pass

# TODO rename load_map
def cache_map(mapnum):

    for plane in range(MAP_PLANES):
        pos = state.mapheaderseg[mapnum].plane_start[plane];
        compressed = state.mapheaderseg[mapnum].plane_length[plane];

        # unhuffman, then unRLEW
        # The huffman'd chunk has a two byte expanded length first
        # The resulting RLEW chunk also does, even though it's not really needed
        state.maphandle.seek(pos)
        bytes_read, expanded_length = readctype(state.maphandle, ctypes.c_ushort)
        source = state.maphandle.read(compressed - bytes_read)

        source_expanded = carmack_expand(source, expanded_length)
        state.mapsegs.append(rlew_expand(source_expanded[2:], de.MAP_AREA * 2))

## internal functions

def setup_map_file():
    with datafile('MAPHEAD') as handle:
        bytes_read, state.RLEWtag = readctype(handle, ctypes.c_ushort)
        header_offsets = []

        length = NUM_MAPS * 4
        while length:
            bytes_read, offset = readctype(handle)
            length -= bytes_read
            header_offsets.append(offset)

    for pos in header_offsets:
        if pos < 0:
            # $FFFFFFFF start is a sparse map
            continue

        state.maphandle.seek(pos)
        map_header = MapHeader()
        state.maphandle.readinto(map_header)
        state.mapheaderseg.append(map_header)


def setup_graphics_file():
    with datafile('VGADICT') as handle:
        node = HuffNode()
        while handle.readinto(node):
            state.grhuffman.append(node)
            node = HuffNode()

    with datafile('VGAHEAD') as handle:
        data = handle.read()

    grstarts = []
    di = 0
    for i in range(gfx.NUMCHUNKS + 1):
        val = data[di] | data[di + 1] << 8 | data[ di + 2] << 16;
        grstarts.append(-1 if val == 0x00FFFFFF else val)
        di += 3

    with datafile('VGAGRAPH') as grhandle:
        # load the pic and sprite headers into the arrays in the data segment
        grhandle.seek(grstarts[0])
        chunkexplen = readctype(grhandle)
        chunkcomplen = grstarts[1] - grstarts[0] - 4
        source = grhandle.read(chunkcomplen)

        pictable_bytes = huff_expand(source, gfx.NUMPICS * ctypes.sizeof(Picture))
        pictable_bytes = BytesIO(pictable_bytes)
        pic = Picture()
        while pictable_bytes.readinto(pic):
            state.pictable.append(pic)
            pic = Picture()

        # instead of loading graphics on demand, load them all on startup
        for chunk in range(gfx.NUMCHUNKS):
            if chunk == 135:
                # this one is not defined in gfx
                continue

            grseg = load_graphic(grhandle, grstarts, chunk)
            state.grsegs.append(grseg)

def load_graphic(grhandle, grstarts, chunk):
    pos = grstarts[chunk]
    if not pos:
        #$FFFFFFFF start is a sparse tile
        return

    next_ = chunk + 1
    while grstarts[next_] == -1:
        next_ += 1

    compressed = grstarts[next_] - pos

    grhandle.seek(pos)

    bytes_read, length = expanded_length(chunk, grhandle)
    source = grhandle.read(compressed - bytes_read)

    return huff_expand(source, length)


def expanded_length(chunk, handle):
    BLOCK = 64
    MASK_BLOCK = 128

    if chunk >= gfx.STARTTILE8 and chunk < gfx.STARTEXTERNS:
        # expanded sizes of tile8/16/32 are implicit

        if chunk < gfx.STARTTILE8M:
            # tile 8s are all in one chunk!
            expanded = BLOCK * gfx.NUMTILE8
        elif chunk < gfx.STARTTILE16:
            expanded = MASKBLOCK * gfx.NUMTILE8M
        elif chunk < gfx.STARTTILE16M:
            # all other tiles are one/chunk
            expanded = BLOCK * 4
        elif chunk < gfx.STARTTILE32:
            expanded = MASKBLOCK * 4
        elif chunk < gfx.STARTTILE32M:
            expanded = BLOCK * 16
        else:
            expanded = MASKBLOCK * 16

        return 0, expanded
    else:
        # everything else has an explicit size longword
        return readctype(handle)


def setup_audio_file():
    pass


def huff_expand(source, length):
    dest = bytearray()
    headptr = 254         # head node is always node 254
    huffptr = headptr

    written = 0
    source = (b for b in source)
    val = next(source)
    mask = 1

    while True:

        if not (val & mask):
            nodeval = state.grhuffman[huffptr].bit0
        else:
            nodeval = state.grhuffman[huffptr].bit1

        if mask == 0x80:
            val = next(source)
            mask = 1;
        else:
            mask = mask << 1;

        if nodeval < 256:
            dest.append(nodeval)
            huffptr = headptr
            if len(dest) >= length:
                break
        else:
            huffptr = nodeval - 256

    return dest

def carmack_expand(source, length):
    NEAR_TAG = 0xa7
    FAR_TAG = 0xa8

    length = length // 2
    source = bytearray(source)
    dest = bytearray()

    while length > 0:
        ch = read_word(source, byteorder='little')
        ch_high = ch >> 8

        if ch_high in (NEAR_TAG, FAR_TAG):
            count = ch & 0xff;
            if not count:
                # have to insert a word containing the tag byte
                ch |= source.pop(0)
                write_word(dest, ch)

                length -= 1;
            elif ch_high == NEAR_TAG:
                offset = source.pop(0)
                length -= count;

                if length >= 0:
                    start = -offset * 2
                    end = (-offset + count) * 2
                    if (-offset + count) >= 0:
                        end = len(dest)
                    dest += dest[start : end]

            elif ch_high == FAR_TAG:
                offset = read_word(source, byteorder='little')
                length -= count
                if length >= 0:
                    dest += dest[offset*2 : (offset + count) *2]

        else:
            write_word(dest, ch)
            length -= 1;

    return dest

def rlew_expand(source, length):
    dest = bytearray()

    while len(dest) < length:

        value = read_word(source)
        if value != state.RLEWtag:
            # uncompressed
            write_word(dest, value)
        else:
            # compressed string
            count = read_word(source)
            value = read_word(source)
            for i in range(count):
                write_word(dest, value)

    return dest
