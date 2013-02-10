from django.conf import settings
from django.http import HttpResponseForbidden


def get_sms_callback_ips():
    return getattr(settings, 'SMS_CALLBACK_IPS', '')


def ip_restrictions(func):
    def _decorated(*args, **kwargs):
        request = args[0]
        request_ip = request.META['REMOTE_ADDR']

        sms_callback_ips = get_sms_callback_ips()

        if sms_callback_ips and request_ip not in sms_callback_ips:
            return HttpResponseForbidden()

        return func(*args, **kwargs)
    return _decorated
