# -*- coding: utf-8 -*-
from smsapi import SMSApi
from sms.models import SmsReceive, SmsQueue
from datetime import datetime

SMS_CALLBACK_IPS = ['46.4.31.8', '62.181.2.52']

class Gateway():
    
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
        try:
            result = self.api.getSenders()
        except AttributeError:
            result = []
        return result

    def callback_received_sms(self, request_data):
        if request_data.get('sms_from', None):
            sms_date_sent = datetime.fromtimestamp(float(request_data.get('sms_date',0))).strftime("%Y-%m-%d %H:%M:%S")

            sms = SmsReceive()
            sms.sender = request_data.get('sms_from', None)
            sms.recipient = request_data.get('sms_to', None)
            sms.content = request_data.get('sms_text', None)
            sms.date_sent = sms_date_sent
            
            try:
                parent_sms = SmsQueue.objects.get(sms_id=request_data.get('MsgId', None))
            except SmsQueue.DoesNotExist:
                pass
            else:
                sms.parent_sms = parent_sms
            
            sms.save()

            return 'OK'

        return ''

    def _get_list_from_request_data(self, request_data, name):
        return request_data.get(name, '').split(',')
        
    def callback_delivery_report(self, request_data):
        if request_data.get('MsgId', None):
            msg_ids = self._get_list_from_request_data(request_data, 'MsgId')
            msg_statuses = self._get_list_from_request_data(request_data, 'status')
            msg_delivery_date = self._get_list_from_request_data(request_data, 'donedate')
            
            for index in range(0, len(msg_ids)):
                try:
                    sms = SmsQueue.objects.get(sms_id=msg_ids[index])
                except SmsQueue.DoesNotExist:
                    pass
                else:
                    if msg_statuses[index] == '404':
                        sms.status = 'delivered'
                    elif msg_statuses[index] == '405':
                        sms.status = 'not_delivered'

                    sms.save()
                    
            return 'OK'
        
        return ''


