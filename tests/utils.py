#!/usr/bin/env python
# coding=utf-8

"""Utilities for tests."""

import random


def gen_otp_secret():
    """Generate OTP secret."""
    return ("").join([
        random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ234567")
        for ignore in range(16)
    ])
