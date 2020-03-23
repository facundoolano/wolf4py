# From ID_CA.H / ID_CA.CPP
# Loads and decompresses asset files and makes the available at RAM.
import id_video_low as vl
import gfxv_wl6 as gfx
import ctypes

class HuffNode(ctypes.Structure):
    _fields_ = [('bit0', ctypes.c_ushort),
                ('bit1', ctypes.c_ushort)]

def datafile(filename):
    return open('data/{}.WL6'.format(filename), 'rb')

class CacheState():
    grstarts = []
    grhuffman = []

    grhandle = datafile('VGAGRAPH')

state = CacheState()

def startup():
    setup_map_file()
    setup_graphics_file()
    setup_audio_file()

def shutdown():
    pass

# TODO rename load_picture
def cache_screen(chunk):
    pos = state.grstarts[chunk]
    next_ = chunk + 1
    while state.grstarts[next_] == -1:
        next_ += 1
    compressed = state.grstarts[next_] - pos

    state.grhandle.seek(pos)

    # first part of the segment contains the expanded length
    # TODO maybe move into huffexpand?
    length_t = ctypes.c_int32()
    state.grhandle.readinto(length_t)
    expanded_length = length_t.value
    source = state.grhandle.read(compressed - ctypes.sizeof(length_t))

    pic = huff_expand(source, expanded_length)
    # TODO better to return bytes and call the drawing elsewhere
    vl.draw_surface(pic)

# TODO rename load_map
def cache_map(mapnum):
    pass


## internal functions

def setup_map_file():
    pass

def setup_graphics_file():
    with datafile('VGADICT') as handle:
        node = HuffNode()
        while handle.readinto(node):
            state.grhuffman.append(node)
            node = HuffNode()

    with datafile('VGAHEAD') as handle:
        data = handle.read()

    di = 0
    for i in range(gfx.NUMCHUNKS + 1):
        val = data[di] | data[di + 1] << 8 | data[ di + 2] << 16;
        state.grstarts.append(-1 if val == 0x00FFFFFF else val)
        di += 3

    # FIXME load the pic and sprite headers into the arrays in the data segment


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
