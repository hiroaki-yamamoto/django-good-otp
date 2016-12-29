#!/usr/bin/env python
# coding=utf-8
"""Setup script."""

import json
from os.path import dirname, join
import sys
from setuptools import setup, find_packages

package_dct = {}
with open(join(dirname(__file__), "package.json")) as package:
    package_dct = json.load(package)

dependencies = ("pyotp", "qrcode", "django", "jinja2")
keywords = (" ").join(package_dct["keywords"])

author = "Hiroaki Yamamoto"
author_email = "hiroaki@hysoftware.net"

if sys.version_info < (2, 7):
    raise RuntimeError("Not supported on earlier then python 2.7.")

try:
    with open(join(dirname(__file__), "README.rst")) as readme:
        long_desc = readme.read()
except Exception:
    long_desc = None

setup_kwargs = {
    key: value for (key, value) in package_dct.items()
    if key in {
        "name", "description", "url", "license", "version"
    }
}
setup_kwargs.update({
    "long_description": long_desc,
    "url": "https://github.com/hiroaki-yamamoto/django-good-otp",
    "packages": find_packages(exclude=["tests"]),
    "include_package_data": True,
    "install_requires": dependencies,
    "zip_safe": False,
    "keywords": keywords,
    "classifiers": [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5"
    ]
})

setup(**setup_kwargs)
