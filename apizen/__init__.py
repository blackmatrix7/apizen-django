from django.conf import settings
from importlib import import_module


def auto_register_webapi():
    for method in settings.APIZEN_WEBAPI:
        import_module(method)
