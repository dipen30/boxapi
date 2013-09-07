#!/usr/bin/env python
from distutils.core import setup
from box import __version__

setup(name="box",
      version=__version__,
      description="Box library for python",
      license="MIT",
      author="Dipen Patel",
      author_email="patel.dipen30@gmail.com",
      url="http://github.com/boxapi/box",
      packages=['box'],
      keywords="box library")
