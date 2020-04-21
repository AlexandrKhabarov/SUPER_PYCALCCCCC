import os
import unittest

from setuptools import setup, find_packages

root_dir = os.path.dirname(__file__)


def pycalc_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(os.path.join(root_dir, 'tests'), pattern='test_*.py')
    return test_suite


setup(
    name='pycalc',
    version='0.0.1',
    description="Pure-python command-line calculator.",
    license='Apache License 2.0',
    author="Alexander Khabarov",
    author_email="rob.sumsung.mi3@gmail.com",
    packages=find_packages(exclude=['tests*']),
    test_suite='setup.pycalc_test_suite',
    url="https://github.com/AlexandrKhabarov/pycalc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pycalc = pycalc.main:main',
        ]
    },
    python_requires='~=3.6',
)
