import cffi

ffi = cffi.FFI()

ffi.embedding_api("""
    int add1(int, int);
""")

ffi.embedding_init_code(r"""
    from _tlocal_cffi import ffi
    import itertools
    try:
        import thread
        g_seen = itertools.count().next
    except ImportError:
        import _thread as thread      # py3
        g_seen = itertools.count().__next__
    tloc = thread._local()

    @ffi.def_extern()
    def add1(x, y):
        try:
            num = tloc.num
        except AttributeError:
            num = tloc.num = g_seen() * 1000
        return x + y + num
""")

ffi.set_source("_tlocal_cffi", """
""")

fn = ffi.compile(verbose=True)
print('FILENAME: %s' % (fn,))
