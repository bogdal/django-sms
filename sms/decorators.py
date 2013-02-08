from django.conf import settings
from django.http import HttpResponseForbidden


SMS_CALLBACK_IPS = getattr(settings, 'SMS_CALLBACK_IPS')


def ip_restrictions(func):
    def _decorated(*args, **kwargs):
        request = args[0]
        request_ip = request.META['REMOTE_ADDR']
        
        if SMS_CALLBACK_IPS and request_ip not in SMS_CALLBACK_IPS:
            return HttpResponseForbidden()

        return func(*args, **kwargs)
    return _decorated
