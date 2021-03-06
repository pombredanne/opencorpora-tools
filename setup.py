#!/usr/bin/env python
import sys
from distutils.core import setup

for cmd in ('egg_info', 'develop'):
    if cmd in sys.argv:
        from setuptools import setup

__version__ = '0.1'

PY3 = sys.version_info[0] == 3
if not PY3:
    reload(sys)
    sys.setdefaultencoding("utf-8")

setup(
    name = 'opencorpora-tools',
    version = __version__,
    author = 'Mikhail Korobov',
    author_email = 'kmike84@gmail.com',
    url = 'https://github.com/kmike/opencorpora-tools/',

    description = 'opencorpora.org python interface',
    long_description = open('README.rst').read(),

    license = 'MIT license',
    packages = ['opencorpora'],
    scripts=['bin/opencorpora'],
    requires = ['argparse', 'ordereddict'],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Text Processing :: Linguistic',
    ],
)
