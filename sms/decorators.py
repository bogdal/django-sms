# -*- coding: utf-8 -*-
from django.conf import settings
from django.utils.importlib import import_module
from django.http import HttpResponse
import sms

def ip_restrictions(func):
    def _decorated(*args, **kwargs):
        request = args[0]
        request_ip = request.META['REMOTE_ADDR']
        
        try:
            restricted_ips = settings.SMS_CALLBACK_IPS
        except AttributeError:
            restricted_ips = sms.SMS_CALLBACK_IPS
        
        if request_ip in restricted_ips:
            return func(*args, **kwargs)
        else:
            return HttpResponse(status=403)
    return _decorated

def is_implemented(func):
    """
    
    """
    def _decorated(*args, **kwargs):
        func_name = func.__name__

        try:
            args = (args[1],)
        except IndexError:
            args = ()
            
        try:       
            module = import_module(settings.SMS_GATEWAY)
        except AttributeError:
            raise NotImplementedError("Parameter settings.SMS_GATEWAY does not exist")
        else:
            gateway = module.Gateway()
        
        if func_name in dir(module.Gateway):
            method = getattr(gateway, func_name)
            return method(*args, **kwargs)
        else:
            class_name = "%s.%s" % (gateway.__class__.__module__, gateway.__class__.__name__)
            raise NotImplementedError("Method '%s' does not exist in '%s'" % (func_name, class_name))
        
        return func(*args, **kwargs)
    return _decorated