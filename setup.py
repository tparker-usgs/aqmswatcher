"""
aqmswatcher -- keep an eye on AQMS

"""

from setuptools import setup, find_packages
from aqmswatcher import __version__

DOCSTRING = __doc__.split("\n")

setup(
    name="aqmswatcher",
    version=__version__,
    author="Tom Parker",
    author_email="tparker@usgs.gov",
    description=(DOCSTRING[1]),
    license="CC0",
    url="http://github.com/tparker-usgs/aqmswatcher",
    packages=find_packages(),
    long_description='\n'.join(DOCSTRING[3:]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Topic :: Software Development :: Libraries",
        "License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication",
    ],
    install_requires=[
        'tomputils>=1.12.16',
        'geojson'
    ],
    entry_points={
        'console_scripts': [
            'check_comcat = aqmswatcher.check_comcat:main'
        ]
    }
)
