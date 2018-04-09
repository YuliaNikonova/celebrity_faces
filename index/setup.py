from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy


def get_extension(name):
    python_path = 'python/{}.pyx'.format(name)
    cplus_path = 'nsw/{}.cpp'.format(name)

    return Extension(
        name,
        [python_path, cplus_path],
        language='c++',
        include_dirs=['nsw', numpy.get_include()]
        # extra_compile_args=['-O3', '-Wall'],
        # extra_link_args=['-g'],
        # libraries = ["dv",],
    )

extention_names = ['node', 'nsw']
extensions = [get_extension(name) for name in extention_names]

setup(
    name='nsw',
    version='0.0.1',
    description='Navigable Small Worlds package',
    ext_modules=extensions,
    cmdclass={'build_ext': build_ext}
)
