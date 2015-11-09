#!/usr/bin/env python
"""
    Pip module setup
"""
from setuptools import setup

INSTALL_REQUIRES = [
    'docopt >= 0.6.1, < 0.7',
    'PyYAML >= 3.10, < 4',
    'six >= 1.3.0, < 2',
    'jsonschema >= 2.5.1, < 3',
]

setup(name='docker-compress',
      provides=["compress"],
      version='0.1.1',
      description='Docker compose file merger',
      url='http://github.com/michaeljs1990/compress',
      author='Michael Schuett',
      author_email='michaelj1990@gmail.com',
      license='MIT',
      install_requires=INSTALL_REQUIRES,
      entry_points="""
      [console_scripts]
      docker-compress = compress.cli.main:main
      """,)
