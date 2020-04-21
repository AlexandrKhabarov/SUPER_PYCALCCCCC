# Python Programming Language Foundation Hometask
In this repository implemented pure-python command-line calculator
using **python 3.6**.

Calculator provides the following interface:
```shell
$ pycalc --help
usage: pycalc [-h] [-m MODULE [MODULE ...]] EXPRESSION

Pure-python command-line calculator.

positional arguments:
  EXPRESSION            expression string to evaluate

optional arguments:
  -h, --help            show this help message and exit
  -m MODULE [MODULE ...], --use-modules MODULE [MODULE ...]
                        additional modules to use
```

In case of any mistakes in the expression utility print human-readable
error explanation **with "ERROR: " prefix**:
```shell
$ pycalc '15(25+1'
ERROR: brackets are not balanced
$ pycalc 'sin(-Pi/4)**1.5'
ERROR: negative number cannot be raised to a fractional power
```

### Supported mathematical operations
* arithmetic (`+`, `-`, `*`, `/`, `//`, `%`, `^`, `**`) (`^` is a power)
* comparison (`<`, `<=`, `==`, `!=`, `>=`, `>`)
* built-in python functions (`abs`, `pow`, `round`)
* functions from standard python module math (trigonometry, logarithms, etc.)
* functions and constants from modules provided with `--use-modules` option

### Distribution
* Utility is wrapped into distribution package with `setuptools`.
* Package export CLI utility named `pycalc`.
