"""
smsAPI.pl
"""
from django.conf import settings
from suds.client import Client
from suds import WebFault
import urllib2
from sms import SmsError

class SMSApi(object):

    def __init__(self):
        self.server = Client('https://www.smsapi.pl/webservices/v2/?wsdl')
        self.client = {'username': settings.SMSAPI_LOGIN,'password': settings.SMSAPI_PASS}
    
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
            result = self.server.service.send_sms(client=self.client,sms=param)
        except WebFault as e:
            raise SmsError(e)

        return result['response'][0]['id']
	
    def getSenders(self):
        result = self.server.service.get_senders(**self.client)
        return result['senders']
        
    def getPoints(self):
        smsUrl = 'http://api.smsapi.pl/send.do?username=%s&password=%s&points=1&details=1' % (
                settings.SMSAPI_LOGIN,
                settings.SMSAPI_PASS,
            )
            
        request = urllib2.Request(smsUrl)
        result = urllib2.urlopen(request)
        response = result.read()
        
        result = {
            "available_points": response[response.find(":")+1:response.find(";")],
            "pro_sms": response[response.find(";")+1:response.rfind(";")],
            "eco_sms": response[response.rfind(";")+1:],
        }
        
        return result
