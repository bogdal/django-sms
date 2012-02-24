# -*- coding: utf-8 -*-
from django.utils.importlib import import_module
from django.conf import settings

class Gateway:

    sms_callback_ips = ['127.0.0.1'] # The IPS which have access to views for callbacks
    
    def __init__(self):
        
        try:       
            module = import_module(settings.SMS_GATEWAY)
        except AttributeError:
            raise NotImplementedError("Parameter settings.SMS_GATEWAY does not exist")
        else:
            gateway = module.Gateway()
        
        self.sms_callback_ips = gateway.sms_callback_ips    
        self.gateway = gateway
    
    def send_sms(self, sms_obj):
        return self.gateway.send_sms(sms_obj)

    def get_senders_list(self):
        return self.gateway.get_senders_list()

    def callback_received_sms(self, request_data):
        return self.gateway.callback_received_sms(request_data)

    def callback_delivery_report(self, request_data):
        return self.gateway.callback_received_sms(request_data)
