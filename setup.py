from distutils.core import setup


setup(
    name = 'ipromise',
    packages = ['ipromise'],
    version = '0.1',
    description = 'A Python base class that provides various decorators for specifying promises relating to inheritance.',
    author = 'Neil Girdhar',
    author_email = 'mistersheik@gmail.com',
    url = 'https://github.com/NeilGirdhar/ipromise',
    download_url = 'https://github.com/neilgirdhar/ipromise/archive/0.1.tar.gz',
    keywords = ['testing', 'logging', 'example'], # arbitrary keywords
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
)
