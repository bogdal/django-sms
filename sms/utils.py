from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_required_param(parameter):
    if not hasattr(settings, parameter):
        raise ImproperlyConfigured("Parameter '%s' does not exist in settings file" % parameter)
    return getattr(settings, parameter)
