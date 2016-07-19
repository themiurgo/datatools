#!/usr/bin/env python
"""A package that makes data-wringling at commandline a matter of pipes."""
from setuptools import find_packages, setup

setup(name = 'datatools',
    version = '0.1',
    description = "Data Tools",
    long_description = "Data Tools",
    author="Antonio Lima",
    author_email="anto87@gmail.com",
    url="http://github.com/themiurgo/datatools",
    license = "MIT",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'drandom = datatools.cli:drandom',
            'ddescribe = datatools.cli:describe',
            'dcompute = datatools.cli:compute',
            'dunique = datatools.cli:dunique',
            'dbyrow = datatools.cli:byrow',
            'djoin = datatools.cli:join',
            'dj2gj = datatools:json2geojson',
            'djsonexplorer = datatools.cli:jsonexplorer',
            'dgrep = datatools.cli:grep',
        ],
    },
    scripts=[
        'datatools/external/cols',
        'datatools/external/body',
        'datatools/external/header',
    ]
)