import ctypes

def datafile(filename):
    return open('data/{}.WL6'.format(filename), 'rb')

def readctype(handle, type_=ctypes.c_int32):
    """
    Read into a ctypes var of the given type, return the amount of bytes read
    and its value.
    """
    var = type_()
    bytes_read = handle.readinto(var)

    if isinstance(var, ctypes.Array):
        return bytes_read, var
    else:
        return bytes_read, var.value
