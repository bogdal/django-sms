# -*- coding: utf-8 -*-
from sms.decorators import is_implemented

class Gateway:
    
    @is_implemented
    def send_sms(self, sms_obj): pass

    @is_implemented
    def get_senders_list(self): pass

    @is_implemented
    def callback_received_sms(self, request_data): pass

    @is_implemented
    def callback_delivery_report(self, request_data): pass