#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='ipromise',
    version='1.5',
    description=('A Python base class that provides various decorators for '
                 'specifying promises relating to inheritance.'),
    long_description_content_type='text/x-rst',
    author='Neil Girdhar',
    author_email='mistersheik@gmail.com',
    project_urls={
        "Bug Tracker": "https://github.com/NeilGirdhar/ipromise/issues",
        "Source Code": "https://github.com/NeilGirdhar/ipromise",
    },
    download_url = "https://pypi.python.org/pypi/ipromise",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    keywords=['testing', 'logging', 'example'],
    python_requires='>=3.7',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
