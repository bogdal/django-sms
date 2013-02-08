from django.http import HttpResponse
from sms.gateway.sms_gateway import SmsGateway


def callback_delivery_report(request):
    gateway = SmsGateway()
    result = gateway.callback_delivery_report(request.GET or request.POST)
    return HttpResponse(result)


def callback_received_sms(request):
    gateway = SmsGateway()
    result = gateway.callback_received_sms(request.GET or request.POST)
    return HttpResponse(result)
