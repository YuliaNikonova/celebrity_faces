import os
from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext


def get_extension(name, link_args=[]):
    python_path = 'python/{}.pyx'.format(name)
    cplus_path = 'src/{}.cpp'.format(name)
    link_args.append('-l:{}.so'.format(name))

    return Extension(
        'python.' + name,
        [python_path, cplus_path],
        language='c++',
        include_dirs=['.', 'src', 'python'],
        extra_compile_args=['-O3', '-Wall', '-std=c++11', '-ggdb3'],
        extra_link_args=[
            '-g',
            '-L{}/python'.format(os.path.dirname(os.path.realpath(__file__)))
        ] + link_args[:-1]
    )

extensions = ['node', 'dist', 'nsw', 'index']
extensions = [get_extension(name) for name in extensions]

setup(
    name='index',
    version='0.0.1',
    description='Navigable Small Worlds package',
    ext_modules=cythonize(extensions),
    cmdclass={'build_ext': build_ext}
)
