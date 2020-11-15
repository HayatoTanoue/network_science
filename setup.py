import sys

from setuptools import setup, find_packages

import network_science


setup(
    name='network_science',
    version=network_science.__version__,
    description='network_science functions',
    long_description_content_type="text/markdown",
    long_description=network_science.__doc__,
    url='https://github.com/HayatoTanoue/network_science',
    license='MIT',

    author=network_science.__author__,
    author_email='hayatotanoue7321@gmail.com',

    # include all packages
    packages=find_packages(),

    install_requires=[
        'matplotlib',
        'networkx',
        'numpy',
        'scipy',
        'seaborn'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6'
    ],
)