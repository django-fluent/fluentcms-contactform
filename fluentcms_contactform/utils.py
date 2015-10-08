from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from .compat import lru_cache
from . import appsettings

_ipresolver = None

def import_symbol(import_path):
    """
    Import a class or attribute by name.
    """
    try:
        dot = import_path.rindex('.')
    except ValueError:
        raise ImproperlyConfigured("{0} isn't a Python path.".format(import_path))

    module, classname = import_path[:dot], import_path[dot + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module {0}: "{1}"'.format(module, e))

    try:
        return getattr(mod, classname)
    except AttributeError:
        raise ImproperlyConfigured('Module "{0}" does not define a "{1}" class.'.format(module, classname))



def get_remote_ip(request):
    """
    Find the IP address of the current request.
    This may require reading a different request header depending on the server setup.
    By default this is handled by django-ipware, but you can use your own resolver if needed
    by defining ``FLUENTCMS_CONTACTFORM_IP_RESOLVER``.
    """
    ip_resolver = get_ip_resolver()
    return ip_resolver(request)


@lru_cache()
def get_ip_resolver():
    return import_symbol(appsettings.FLUENTCMS_CONTACTFORM_IP_RESOLVER)
