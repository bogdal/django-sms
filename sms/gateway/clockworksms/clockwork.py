import requests

CLOCKWORK_API_URL = "https://api.clockworksms.com/http/send.aspx"


class Clockwork(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def send_sms(self, number, message, sender):
        data = {
            'key': self.api_key,
            'from': sender,
            'to': number,
            'content': message
        }
        response = requests.post(CLOCKWORK_API_URL, data=data)
        return response.text[response.text.rfind(' ')+1:].strip()
