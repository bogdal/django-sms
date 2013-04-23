from sms.gateway.clockworksms.clockwork import Clockwork
from sms.utils import get_required_param

CLOCKWORK_KEY = get_required_param('CLOCKWORK_KEY')


class ClockworkGateway(object):

    def __init__(self):
        self.api = Clockwork(CLOCKWORK_KEY)

    def send_sms(self, sms):
        sms_id = self.api.send_sms(
            number=sms.recipient,
            message=sms.content,
            sender=sms.sender,
        )

        return sms_id

    def get_senders(self):
        return None

    def callback_received_sms(self, data):
        return 'OK'

    def callback_delivery_report(self, data):
        return 'OK'
