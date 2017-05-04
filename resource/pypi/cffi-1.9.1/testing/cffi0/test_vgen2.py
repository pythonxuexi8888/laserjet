import cffi.verifier
from .test_vgen import *

# This test file runs normally after test_vgen.  We only clean up the .c
# sources, to check that it also works when we have only the .so.  The
# tests should run much faster than test_vgen.

def setup_module():
    cffi.verifier.cleanup_tmpdir(keep_so=True)
    cffi.verifier._FORCE_GENERIC_ENGINE = True

def teardown_module():
    cffi.verifier._FORCE_GENERIC_ENGINE = False
