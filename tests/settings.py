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

USE_I18N = True
