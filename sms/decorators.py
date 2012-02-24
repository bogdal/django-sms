# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.importlib import import_module
from django.http import HttpResponse

def ip_restrictions(func):
    def _decorated(*args, **kwargs):
        
        request = args[0]
        request_ip = request.META['REMOTE_ADDR']
        
        module = import_module(settings.SMS_GATEWAY)
        gateway = module.Gateway()
        
        try:
            restricted_ips = settings.SMS_CALLBACK_IPS
        except AttributeError:
            restricted_ips = gateway.sms_callback_ips
        
        if request_ip in restricted_ips:
            return func(*args, **kwargs)
        else:
            return HttpResponse(status=403)
    return _decorated
