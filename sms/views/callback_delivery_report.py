# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from django.utils.importlib import import_module

def callback_delivery_report(request):

    module = import_module(settings.SMS_GATEWAY)
    gateway = module.Gateway()

    result = gateway.callback_delivery_report(request.POST)

    return HttpResponse(result)