import ctypes
import struct

def datafile(filename):
    return open('data/{}.WL6'.format(filename), 'rb')

def readctype(handle, type_=ctypes.c_int32):
    """
    Read into a ctypes var of the given type, return the amount of bytes read
    and its value.
    """
    var = type_()
    bytes_read = handle.readinto(var)

    if hasattr(var, 'value'):
        return bytes_read, var.value
    else:
        return bytes_read, var


def read_word(source, byteorder='big'):
    """
    Extract 2 bytes from the source and return them as word according to the
    given byteorder.
    """
    pattern = '<H' if byteorder == 'little' else '>H'
    ch, = struct.unpack_from(pattern, source)
    source.pop(0)
    source.pop(0)
    return ch

# FIXME duplicated
def read_short(source, byteorder='big'):
    pattern = '<h' if byteorder == 'little' else '>H'
    ch, = struct.unpack_from(pattern, source)
    source.pop(0)
    source.pop(0)
    return ch

def write_word(dest, word):
    "Add the 2 bytes of the given word to the end of the bytearray."
    dest.extend(word.to_bytes(length=2, byteorder='big'))
