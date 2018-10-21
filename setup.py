from setuptools import setup

setup(
    name='SUPER__PYCALC',
    version='0.0.1',
    description="Pure-python command-line calculator.",
    author="Alexander Khabarov",
    author_email="rob.sumsung.mi3@gmail.com",
    packages=["pycalc", "pycalc.console_app", "pycalc.core"],
    test_suite="pycalc.tests",
    url="https://github.com/AlexandrKhabarov/SUPER_PYCALCCCCC",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'pycalc = pycalc.main:main',
        ]
    }
)
