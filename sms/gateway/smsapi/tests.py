from django.core.urlresolvers import reverse
from django.test import TestCase, Client
from sms.models import Sms, Inbox
import mock


class SmsApiTest(TestCase):

    def setUp(self):
        self.client = Client()

    @mock.patch('sms.decorators.get_sms_callback_ips', return_value='')
    def test_received_sms(self, sms_callback_ips_mock):

        sms_id = 'abcdefgh123456'
        sms_text = 'test message'

        parent_sms = Sms.objects.create(recipient='111222333', content='message', status=Sms.SENT, sms_id=sms_id)

        data = {
            'MsgId': sms_id,
            'sms_from': '111222333',
            'sms_to': '222333444',
            'sms_text': sms_text,
            'sms_date': '1360320274'
        }

        response = self.client.post(reverse('callback-received-sms'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

        received_smses = Inbox.objects.filter(parent_sms=parent_sms, content=sms_text)
        self.assertTrue(received_smses.exists())

    @mock.patch('sms.decorators.get_sms_callback_ips', return_value='')
    def test_delivery_report(self, sms_callback_ips_mock):
        sms_id_1 = 'abcdefgh123456'
        sms_id_2 = 'abcdefgh123457'

        Sms.objects.create(recipient='111222333', content='test message 1', status=Sms.SENT, sms_id=sms_id_1)
        Sms.objects.create(recipient='222333444', content='test message 2', status=Sms.SENT, sms_id=sms_id_2)

        data = {
            'MsgId': sms_id_1,
            'status': '404',
            'donedate': '1360320274',
            'username': 'test',
            'points': '1',
            'to': '111111111',
        }

        response = self.client.get(reverse('callback-delivery-report'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

        sms = Sms.objects.get(sms_id=sms_id_1)
        self.assertEqual(sms.status, Sms.DELIVERED)

        data.update({
            'MsgId': sms_id_2,
            'status': '405'
        })
        response = self.client.get(reverse('callback-delivery-report'), data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')

        sms = Sms.objects.get(sms_id=sms_id_2)
        self.assertEqual(sms.status, Sms.NOT_DELIVERED)