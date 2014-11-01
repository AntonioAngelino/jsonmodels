#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup."""

import os
import sys

from setuptools.command.test import test as TestCommand
from jsonmodels import __version__ as version

from setuptools import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

# Hacking unittest.
try:
    import tests
    if 'test' in sys.argv and '--quick' in sys.argv:
        tests.QUICK_TESTS = True
        del sys.argv[sys.argv.index('--quick')]

    if 'test' in sys.argv and '--spelling' in sys.argv:
        tests.CHECK_SPELLING = True
        del sys.argv[sys.argv.index('--spelling')]
except ImportError:
    pass

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='jsonmodels',
    version=version,
    description='Models to make easier to deal with structures that'
    ' are converted to, or read from JSON.',
    long_description=readme + '\n\n' + history,
    author='Szczepan Cieślik',
    author_email='szczepan.cieslik@gmail.com',
    url='https://github.com/beregond/jsonmodels',
    packages=[
        'jsonmodels',
    ],
    package_dir={'jsonmodels': 'jsonmodels'},
    include_package_data=True,
    install_requires=[
        'python-dateutil',
        'six',
    ],
    license="BSD",
    zip_safe=False,
    keywords='jsonmodels',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=[
        'pytest',
    ],
    cmdclass = {
        'test': PyTest,
    },
)
