# -*- coding: utf-8 -*-
from smsapi import SMSApi
from sms.base_gateway import BaseGateway
from sms.models import SmsReceive
from datetime import datetime

class Gateway(BaseGateway):
    def __init__(self):
        self.api = SMSApi()

    def send_sms(self, sms):

        sms_id = self.api.send_sms(
            number = sms.recipient,
            message = sms.content,
            sender = sms.sender,
            eco=sms.eco,
            flash=sms.flash,
            test=sms.test
        )

        return sms_id

    def get_senders_list(self):
        return self.api.getSenders()

    def callback_received_sms(self, POST):

        if POST.get('sms_from', None):
            smsDate = datetime.fromtimestamp(float(POST.get('sms_date',0))).strftime("%Y-%m-%d %H:%M:%S")

            sms = SmsReceive()
            sms.sender = POST.get('sms_from', None)
            sms.recipient = POST.get('sms_to', None)
            sms.content = POST.get('sms_text', None)
            sms.sendDate = smsDate
            sms.save()

            return 'OK'

        return ''

    def callback_delivery_report(self, POST):
        #TODO
        return ''


