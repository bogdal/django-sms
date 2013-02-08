from datetime import datetime
from sms.gateway.smsapi.api import Api
from sms.utils import get_required_param

SMSAPI_LOGIN = get_required_param('SMSAPI_LOGIN')
SMSAPI_PASS = get_required_param('SMSAPI_PASS')


class SmsApiGateway(object):
    
    def __init__(self):
        self.api = Api(SMSAPI_LOGIN, SMSAPI_PASS)

    def send_sms(self, sms):
        sms_id = self.api.send_sms(
            number=sms.recipient,
            message=sms.content,
            sender=sms.sender,
            eco=sms.eco,
            flash=sms.flash,
            test=sms.test
        )

        return sms_id

    def get_senders(self):
        try:
            result = self.api.get_senders()
        except AttributeError:
            result = []
        return result

    def callback_received_sms(self, request_data):
        from sms.models import Inbox, Sms
        if request_data.get('sms_from', None):
            sms = Inbox()
            sms.sender = request_data.get('sms_from', None)
            sms.recipient = request_data.get('sms_to', None)
            sms.content = request_data.get('sms_text', None)
            sms.date_sent = self._date_from_unixtime_to_str(request_data.get('sms_date', 0))
            
            try:
                parent_sms = Sms.objects.get(sms_id=request_data.get('MsgId', None))
            except Sms.DoesNotExist:
                pass
            else:
                sms.parent_sms = parent_sms
            
            sms.save()

            return 'OK'
        return ''

    def _date_from_unixtime_to_str(self, date):
        return datetime.fromtimestamp(float(date)).strftime("%Y-%m-%d %H:%M:%S")
    
    def _get_list_from_request_data(self, request_data, name):
        return request_data.get(name, '').split(',')
        
    def callback_delivery_report(self, request_data):
        from sms.models import Inbox, Sms
        if request_data.get('MsgId', None):
            msg_ids = self._get_list_from_request_data(request_data, 'MsgId')
            msg_statuses = self._get_list_from_request_data(request_data, 'status')
            msg_delivery_date = self._get_list_from_request_data(request_data, 'donedate')
            
            for index in range(0, len(msg_ids)):
                try:
                    sms = Sms.objects.get(sms_id=msg_ids[index])
                except Sms.DoesNotExist:
                    pass
                else:
                    if msg_statuses[index] == '404':
                        sms.set_status("delivered", self._date_from_unixtime_to_str(msg_delivery_date[index]))
                    elif msg_statuses[index] == '405':
                        sms.set_status("not_delivered", self._date_from_unixtime_to_str(msg_delivery_date[index]))
                    
            return 'OK'
        return ''
