"""
Copyright (C) 2017-2024 Bryant Moscon - bmoscon@gmail.com

Please see the LICENSE file for the terms and conditions
associated with this software.
"""

import os

from Cython.Build import cythonize
from setuptools import Extension, setup

extra_compile_args = ["/O2" if os.name == "nt" else "-O3"]
define_macros = []

# comment out line to compile with type check assertions
# verify value at runtime with cryptofeed.types.COMPILED_WITH_ASSERTIONS
define_macros.append(("CYTHON_WITHOUT_ASSERTIONS", None))

extension = Extension(
    "cryptofeed.types",
    ["cryptofeed/types.pyx"],
    extra_compile_args=extra_compile_args,
    define_macros=define_macros,
)

setup(
    ext_modules=cythonize([extension], language_level=3, force=True),
)
