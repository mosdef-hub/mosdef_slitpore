from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

setup(
    name='mosdef_slitpore',
    version='0.0',
    description='routines and functions for graphene slitpore simulations',
    author='Ray Matsumoto',
    author_email='ray.a.matsumoto@vanderbilt.edu',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
)
