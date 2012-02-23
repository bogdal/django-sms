# -*- coding: utf-8 -*-

class BaseGateway:

    def send_sms(self, sms_obj):
        pass

    def get_senders_list(self):
        pass

    def callback_received_sms(self, request_data):
        pass

    def callback_delivery_report(self, request_data):
        pass
