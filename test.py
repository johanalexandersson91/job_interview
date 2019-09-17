#!/usr/bin/env python
import sys
import os
import logging
import unittest

from backend import include_paths

logging.getLogger().setLevel(logging.WARN)

# TODO: At the end of tests, there's an ELIFECYCLE error. Tests work anyway, but should
# be looked into.


def flake8():
    print "======================================================================"
    print "Flake8"
    print "======================================================================"

    try:
        from flake8.engine import get_style_guide
    except ImportError:
        print "not installed. run pip install flake8"
        return 0

    flake8_style = get_style_guide(paths=["backend"], exclude="backend/lib/*", max_complexity=12, ignore="E501,E401,E302,W293")

    report = flake8_style.check_files()
    report.print_statistics()

    if not report.total_errors:
        print "OK"

    return report.total_errors

def test():


	# Check if API_key is supplied. This is later read in the testcase itself.
	# Very ugly, but I was out of time.
    if len(sys.argv) != 2:
    	print "ERROR:  missing api key. Exiting"
    	sys.exit(-1)
    	
    
    print "======================================================================"
    print "Running tests"
    print "======================================================================"
    
    

    suite = unittest.TestLoader().discover('backend/test', pattern="test_*.py")

    result = unittest.TextTestRunner(stream=sys.stdout).run(suite)

    return len(result.failures) + len(result.errors)

def test_coverage():
    try:
        from coverage import coverage

        cov = coverage(include="backend/*", omit=["backend/test/*", "*__init__*", "backend/lib/*"])
        print cov		
        cov.start()
        failures = test()
        cov.stop()

        print "======================================================================"
        print "Coverage report"
        print "======================================================================"

        cov.report()
    except ImportError:
        failures = test()

        print "======================================================================"
        print "Coverage report"
        print "======================================================================"

        print "not installed. run pip install coverage"

    return failures


if __name__ == "__main__":
    [sys.path.insert(0, path) for path in include_paths() if path not in sys.path]

    failures = flake8()
    failures += test_coverage()

    print "======================================================================"
    print "Done!"

    exit(failures != 0)
