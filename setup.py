"""
Setup script.
"""

import sys
from distutils.core import Command
from setuptools import setup
from setuptools.command.test import test as TestCommand


class Coverage(Command):
    """
    Coverage setup.
    """

    description = (
        "Run test suite against single instance of"
        "Python and collect coverage data."
    )
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import coverage
        import unittest

        cov = coverage.coverage(config_file='.coveragerc')
        cov.erase()
        cov.start()

        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(start_dir='tests')
        unittest.TextTestRunner().run(test_suite)

        cov.stop()
        cov.save()
        cov.report()
        cov.html_report()


class Tox(TestCommand):
    """
    Tox setup.
    """

    description = "Run test suite against all supported Python interpreters."
    user_options = [('tox-args=', 'a', 'Arguments to pass to tox.')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.tox_args = ''

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import shlex
        import tox

        errno = tox.cmdline(args=shlex.split(self.tox_args))
        sys.exit(errno)


setup(
    author='MingChan',
    author_email='nick.ccm1122@gmail.com',
    description='td_exam_booker',
    download_url='',
    cmdclass={},
    install_requires=[
        'beautifulsoup4',
        'selenium'
    ],
    license='',
    name='td_exam_booker',
    packages=[
        'td_exam_booker',
    ],
    scripts=[],
    entry_points={
        'console_scripts': ['tdexam=td_exam_booker.main:main'],
    },
    tests_require=[
        'codecov>=2.0.3,<3.0.0',
        'coverage>=4.0.3,<5.0.0',
        'Sphinx>=1.4.1,<2.0.0',
        'tox>=2.3.1,<3.0.0',
        'virtualenv>=15.0.1,<16.0.0'
    ],
    url='',
    version='1.0.0'
)
