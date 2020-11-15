from setuptools import setup, find_packages

import network_science


setup(
    name='network_science',
    version=network_science.__version__,
    description='network_science functions',
    long_description=slashcommands.__doc__,
    url='https://github.com/HayatoTanoue/network_science',
    license='MIT',

    author=slashcommands.__author__,
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