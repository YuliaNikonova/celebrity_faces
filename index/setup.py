import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext


def get_extension(name):
    python_path = 'python/{}.pyx'.format(name)
    cplus_path = 'nsw/{}.cpp'.format(name)
    link_args = []
    if name != 'node':
        link_args = ['-l:node.so']

    return Extension(
        'python.' + name,
        [python_path, cplus_path],
        language='c++',
        include_dirs=['.', 'nsw', 'python'],
        extra_compile_args=['-O3', '-Wall', '-std=c++11'],
        extra_link_args=[
            '-g',
            '-L{}/python'.format(os.path.dirname(os.path.realpath(__file__)))
        ] + link_args
    )

extensions = ['node', 'dist', 'nsw']
extensions = [get_extension(name) for name in extensions]

setup(
    name='nsw',
    version='0.0.1',
    description='Navigable Small Worlds package',
    ext_modules=cythonize(extensions),
    cmdclass={'build_ext': build_ext}
)
