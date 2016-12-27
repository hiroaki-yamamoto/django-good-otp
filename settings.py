#!/usr/bin/env python
# coding=utf-8

"""Django Settings to use database-schema migration."""

import os

SECRET_KEY = "test"
ROOT_URLCONF = "django_otp.urls"
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_otp.DjangoOTP",
)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'devel.db'),
    }
}

PASSWORD_HASHERS = ("django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",)
AUTHENTICATION_BACKENDS = ("django_otp.backends.OTPAuthBackend", )

USE_I18N = True
