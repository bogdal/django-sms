# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module

def callback_received_sms(request):

    module = import_module(settings.SMS_GATEWAY)
    gateway = module.Gateway()

    result = gateway.callback_received_sms(request.POST)

    return HttpResponse(result)