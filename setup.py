import os
from setuptools import find_packages, setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='python-geomark',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    license='BSD2',
    description='Tools for manipulating Geomark datasets',
    long_description=README,
    url='https://github.com/greg-and-adam/',
    author='Adam Valair, Greg Sebastian',
    author_email='adam@bitspatial.com, gregseb@protonmail.com',
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Practitioners',
        'License :: OSI Approved :: BSD2',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: Utilities',
    ],
    test_suite="tests"
)