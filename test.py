#!/usr/bin/env python
#
# Runs all tests for Myokit.
#
# This file is part of Myokit
#  Copyright 2011-2018 Maastricht University, University of Oxford
#  Licensed under the GNU General Public License v3.0
#  See: http://myokit.org
#
# Parts of this test script are based on the test script for Pints
# See: https://github.com/pints-team/pints
#
from __future__ import absolute_import, division
from __future__ import print_function, unicode_literals
import sys
import argparse
import unittest
import subprocess


def run_unit_tests(executable=None):
    """
    Runs unit tests, exits if they don't finish.

    If an ``executable`` is given, tests are run in subprocesses using the
    given executable (e.g. ``python2`` or ``python3``).
    """
    if executable is None:
        suite = unittest.defaultTestLoader.discover(
            'tests', pattern='test*.py')
        unittest.TextTestRunner(verbosity=2).run(suite)
    else:
        print('Running unit tests with executable `' + executable + '`')
        cmd = [executable] + [
            '-m',
            'unittest',
            'discover',
            '-v',
            'tests',
        ]
        p = subprocess.Popen(cmd)
        try:
            ret = p.wait()
        except KeyboardInterrupt:
            try:
                p.terminate()
            except OSError:
                pass
            p.wait()
            print('')
            sys.exit(1)
        if ret != 0:
            sys.exit(ret)


def run_flake8():
    """
    Runs flake8 in a subprocess, exits if it doesn't finish.
    """
    print('Running flake8 ... ')
    sys.stdout.flush()
    p = subprocess.Popen(['flake8'], stderr=subprocess.PIPE)
    try:
        ret = p.wait()
    except KeyboardInterrupt:
        try:
            p.terminate()
        except OSError:
            pass
        p.wait()
        print('')
        sys.exit(1)
    if ret == 0:
        print('ok')
    else:
        print('FAILED')
        sys.exit(ret)


def check_docs():
    """
    Checks if the documentation can be built.
    """
    print('Checking if docs can be built.')
    p = subprocess.Popen([
        'sphinx-build',
        'docs/source',
        'docs/build/html',
        '-W',
    ])
    try:
        ret = p.wait()
    except KeyboardInterrupt:
        try:
            p.terminate()
        except OSError:
            pass
        p.wait()
        print('')
        sys.exit(1)
    if ret != 0:
        print('FAILED')
        sys.exit(ret)




if __name__ == '__main__':
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description='Run unit tests for Myokit.',
        epilog='To run individual unit tests, use e.g.'
               ' $ tests/test_parser.py',
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Run quick checks (unit tests, flake8, docs)',
    )
    parser.add_argument(
        '--unit',
        action='store_true',
        help='Run all unit tests using the `python` interpreter.',
    )
    parser.add_argument(
        '--unit2',
        action='store_true',
        help='Run all unit tests using the `python2` interpreter.',
    )
    parser.add_argument(
        '--unit3',
        action='store_true',
        help='Run all unit tests using the `python3` interpreter.',
    )
    parser.add_argument(
        '--nosub',
        action='store_true',
        help='Run all unit tests without starting a subprocess.',
    )
    args = parser.parse_args()

    # Run tests
    has_run = False
    if args.quick:
        has_run = True
        run_flake8()
        run_unit_tests('python')
        check_docs()
    if args.unit:
        has_run = True
        run_unit_tests('python')
    if args.unit2:
        has_run = True
        run_unit_tests('python2')
    if args.unit3:
        has_run = True
        run_unit_tests('python3')
    if args.nosub:
        has_run = True
        run_unit_tests()
    if not has_run:
        parser.print_help()

