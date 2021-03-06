import cffi.verifier
from .test_verify import *


def setup_module():
    cffi.verifier.cleanup_tmpdir()
    cffi.verifier._FORCE_GENERIC_ENGINE = True
    # Runs all tests with _FORCE_GENERIC_ENGINE = True, to make sure we
    # also test vengine_gen.py.

def teardown_module():
    cffi.verifier._FORCE_GENERIC_ENGINE = False
