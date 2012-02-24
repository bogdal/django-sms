from django.utils.importlib import import_module
from django.conf import settings

class SmsError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def sms_callback_ips():
    """ The IPS which have access to views for callbacks """
    
    module = import_module(settings.SMS_GATEWAY)
    try:
        result = module.SMS_CALLBACK_IPS
    except AttributeError:
        raise NotImplementedError("Parameter '%s.SMS_CALLBACK_IPS' does not exist" % settings.SMS_GATEWAY)
    else:
        return result
    
SMS_CALLBACK_IPS = sms_callback_ips()