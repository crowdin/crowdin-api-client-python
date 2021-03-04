# !/usr/bin/env python
import os
import re
import sys
from codecs import open

from setuptools import find_packages, setup
from setuptools.command.test import test

ROOT = os.path.dirname(__file__)
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")


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


with open("README.md", encoding="utf-8") as f:
    README = f.read()


def get_version():
    init = open(os.path.join(ROOT, "crowdin_api", "__init__.py")).read()
    return VERSION_RE.search(init).group(1)


setup(
    name="crowdin-api-client",
    version=get_version(),
    description="Python client library for Crowdin API v2",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Сrowdin",
    author_email="support@crowdin.com",
    url="https://github.com/crowdin/crowdin-api-client-python",
    packages=find_packages(exclude=["*tests*", "*fixtures.py"]),
    package_dir={"crowdin_api": "crowdin_api"},
    python_requires=">=3.6.*",
    license="MIT",
    install_requires=[
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    project_urls={
        "Documentation": "https://support.crowdin.com/api/v2/",
        "Source Code": "https://github.com/crowdin/crowdin-api-client-python",
    },
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
