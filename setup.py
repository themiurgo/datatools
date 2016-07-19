#!/usr/bin/env python
"""A package that makes data-wringling at commandline a matter of pipes."""
from setuptools import find_packages, setup

setup(name = 'datatools',
    version = '0.1.3',
    description = "Data Tools",
    long_description=open('README.md').read(),
    author="Antonio Lima",
    author_email="anto87@gmail.com",
    url="http://github.com/themiurgo/datatools",
    license = "MIT",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'dbyrow = datatools.cli:byrow',
            'dcompute = datatools.cli:compute',
            'ddescribe = datatools.cli:describe',
            'dgrep = datatools.cli:grep',
            'djoin = datatools.cli:join',
            'dj2gj = datatools:json2geojson',
            'djsonexplorer = datatools.cli:jsonexplorer',
            'dunique = datatools.cli:dunique',
            'drandom = datatools.cli:drandom',
        ],
    },
    install_requires=[
        'click',
        'numpy',
        'scipy',
        'six',
        'toolz',
    ],
    scripts=[
        'datatools/external/cols',
        'datatools/external/body',
        'datatools/external/header',
    ]
)