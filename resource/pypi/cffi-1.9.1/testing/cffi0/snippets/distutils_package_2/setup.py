
from distutils.core import setup
import snip_basic_verify2

setup(
    packages=['snip_basic_verify2'],
    ext_package='snip_basic_verify2',
    ext_modules=[snip_basic_verify2.ffi.verifier.get_extension()])
