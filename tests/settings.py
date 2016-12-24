#!/usr/bin/env python
# coding=utf-8


"""Dummy settings."""

DEBUG = True
SECRET_KEY = "secret"
INSTALLED_APPS = ("django_otp", )
DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.sqlite3",
        'NAME': "devel.db"
    }
}
PASSWORD_HASHERS = ("django.contrib.auth.hashers.UnsaltedMD5PasswordHasher",)

USE_I18N = True
