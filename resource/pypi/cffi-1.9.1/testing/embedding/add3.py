import cffi

ffi = cffi.FFI()

ffi.embedding_api("""
    int add3(int, int, int, int);
""")

ffi.embedding_init_code(r"""
    from _add3_cffi import ffi
    import sys

    @ffi.def_extern()
    def add3(x, y, z, t):
        sys.stdout.write("adding %d, %d, %d, %d\n" % (x, y, z, t))
        sys.stdout.flush()
        return x + y + z + t
""")

ffi.set_source("_add3_cffi", """
""")

fn = ffi.compile(verbose=True)
print('FILENAME: %s' % (fn,))
