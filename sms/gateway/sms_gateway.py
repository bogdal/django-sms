from django.utils.importlib import import_module
from sms.utils import get_required_param


SMS_GATEWAY = get_required_param('SMS_GATEWAY')


def current_gateway():
    package, klass = SMS_GATEWAY.rsplit('.', 1)
    module = import_module(package)
    return getattr(module, klass)


class SmsGateway(object):

    def __init__(self):
        self.gateway = current_gateway()()

    def send_sms(self, sms):
        return self.gateway.send_sms(sms)

    def get_senders(self):
        return self.gateway.get_senders()

    def callback_received_sms(self, data):
        return self.gateway.callback_received_sms(data)

    def callback_delivery_report(self, data):
        return self.gateway.callback_delivery_report(data)
