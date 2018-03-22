from importlib import import_module


def autodiscover():
    from django.apps import apps
    for app_config in apps.get_app_configs():
        try:
            import_module('{}.methods'.format(app_config.name))
        except ImportError as ex:
            print(ex)
