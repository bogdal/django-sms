from suds.client import Client
from suds import WebFault
from sms import SmsError


class Api(object):
    """
    smsAPI.pl
    """

    def __init__(self, api_login, api_pass):
        self.server = Client('https://www.smsapi.pl/webservices/v2/?wsdl')
        self.client = {'username': api_login, 'password': api_pass}
    
    def send_sms(self, number, message, sender, eco=True, flash=False, test=False):
        param = {
            'recipient': number,
            'message': message,
            'sender': sender,
            'eco': int(eco),
            'flash': flash,
            'test': int(test),
        }

        try:
            result = self.server.service.send_sms(client=self.client, sms=param)
        except WebFault as e:
            raise SmsError(e)

        return result['response'][0]['id']

    def get_senders(self):
        result = self.server.service.get_senders(**self.client)
        return result['senders']
