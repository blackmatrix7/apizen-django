from django.conf import settings
from importlib import import_module


def auto_import_methods():
    for methods in settings.APIZEN_METHODS:
        import_module(methods)
