import cffi

ffi = cffi.FFI()

ffi.embedding_api("""
    int add2(int, int, int);
""")

ffi.embedding_init_code(r"""
    import sys
    sys.stdout.write("prepADD2\n")

    assert '_add2_cffi' in sys.modules
    m = sys.modules['_add2_cffi']
    import _add2_cffi
    ffi = _add2_cffi.ffi

    @ffi.def_extern()
    def add2(x, y, z):
        sys.stdout.write("adding %d and %d and %d\n" % (x, y, z))
        sys.stdout.flush()
        return x + y + z
""")

ffi.set_source("_add2_cffi", """
""")

fn = ffi.compile(verbose=True)
print('FILENAME: %s' % (fn,))
