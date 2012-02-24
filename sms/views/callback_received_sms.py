# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module
from sms.decorators import ip_restrictions
from sms.gateway import Gateway

@ip_restrictions
def callback_received_sms(request):

    gateway = Gateway()
    result = gateway.callback_received_sms(request.POST)

    return HttpResponse(result)