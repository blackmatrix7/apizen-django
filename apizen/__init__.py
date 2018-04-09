from django.conf import settings
from importlib import import_module


def auto_register_methods():
    for method in settings.APIZEN_METHODS:
        import_module(method)
