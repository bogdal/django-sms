import random


class ExampleGateway(object):

    def send_sms(self, sms):
        return random.randint(1, 1000)

    def get_senders(self):
        return ['example_sender']

    def callback_received_sms(self, data):
        return 'OK'

    def callback_delivery_report(self, data):
        return 'OK'
