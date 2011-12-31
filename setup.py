#!/usr/bin/env python
from erik import __version__

options = {
    'name': 'erik'
    , 'version': __version__
    , 'description': 'a library for vertical wall plotters driven by the EiBot \
        stepper motor controller'
    , 'packages': ['erik']
}

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(**options)

