from distutils.core import setup
from setuptools import setup, find_packages

setup(
    name='pymls',
    version='1.0',
    author='Solomon', 
    author_email='soloemoon@gmail.com',
    packages=find_packages(),
    long_description=open('README.md').read()
)