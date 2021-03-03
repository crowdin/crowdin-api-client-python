# !/usr/bin/env python
import sys
from codecs import open

from setuptools import setup
from setuptools.command.test import test


class PyTest(test):
    def run_tests(self):
        import pytest

        errno = pytest.main(
            [
                "--strict-markers",
                "--tb=short",
                "--doctest-modules",
                "--cov=crowdin_api",
                "--cov-report=term-missing:skip-covered",
                "--cov-report=html",
                "--cov-fail-under=95",
            ]
        )
        sys.exit(errno)


with open("LICENSE") as f:
    LICENSE = f.read()

with open("README.md", "r", "utf-8") as f:
    README = f.read()

setup(
    name="Crowdin api client python",
    version="0.0.0",
    description="Crowdin api client python",
    long_description=README,
    author="Сrowdin",
    # packages=["crowdin-python"],
    package_data={"": ["LICENSE"]},
    package_dir={"crowdin_api": "crowdin_api"},
    python_requires=">=3.6.*",
    install_requires=[
        "requests>=2.25.1",
    ],
    license=LICENSE,
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    cmdclass={"test": PyTest},
    tests_require=[
        "doc8==0.8.1",
        "pytest==6.2.2",
        "pytest-cov==2.11.1",
        "requests-mock==1.8.0",
        "types-six",
        "types-requests",
    ],
)
