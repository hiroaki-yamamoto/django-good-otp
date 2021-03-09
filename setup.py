#!/usr/bin/env python
# coding=utf-8
"""Set up script."""

import os.path as path
import sys
from setuptools import setup, find_packages

author = "Hiroaki Yamamoto"
author_email = "hiroaki@hysoftware.net"
version = "0.0.0"

version_file = path.join(path.abspath(path.dirname(__file__)), "VERSION")

if path.exists(version_file):
    with open(version_file) as v:
        version = v.read()

if sys.version_info < (2, 7):
    raise RuntimeError("Not supported on earlier then python 2.7.")

try:
    with open(path.join(path.dirname(__file__), "README.md")) as readme:
        long_desc = readme.read()
except Exception:
    long_desc = None

setup(
    name="django_good_otp",
    description=(
        "Yet Another Implementation of "
        "One-Time-Password-Authentication for Django"
    ),
    license="MIT",
    version=version,
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url="https://github.com/hiroaki-yamamoto/django-good-otp",
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    install_requires=["pyotp", "qrcode", "django>=1.10", "jinja2"],
    zip_safe=False,
    keywords=["python", "OTP", "Django"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ]
)
