 # -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.models import User
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _
from sms import SmsError

SMS_STATUS = (
     ('not_sent', _("Not sent")),
     ('sent', _("Sent")),
     ('error', _("Dispatch error")),
     ('delivered', _("Delivered")),
     ('not_delivered', _("Not delivered")),
)

class ToSend(models.Manager):
    def get_query_set(self):
        return super(ToSend, self).get_query_set().filter(Q(status="not_sent"), Q(is_active=True))

class SmsQueue(models.Model):
    recipient = models.CharField(max_length=11, verbose_name=_("Recipient"))
    sender = models.ForeignKey('SmsSender', verbose_name=_("Sender"), blank=True, null=True)
    content = models.TextField(verbose_name=_("Message content"), blank=True, null=True)
    flash = models.BooleanField(verbose_name=_("Flash"), default=False)
    test = models.BooleanField(verbose_name=_("Test"), default=False)
    date_created = models.DateTimeField(verbose_name=_("Date created"), auto_now_add=True)
    date_sent = models.DateTimeField(verbose_name=_("Date sent"), blank=True, null=True)
    sms_id = models.CharField(max_length=50, verbose_name=_("Operator sms id"), blank=True, null=True)
    status = models.CharField(max_length = 100, choices = SMS_STATUS, default = 'not_sent', verbose_name=_("Status"), blank = True)
    is_active = models.BooleanField(verbose_name=_("Is active?"), default=True)
    
    objects = models.Manager()
    toSend = ToSend()
    
    def __unicode__(self):
        return unicode(self.recipient)

    @property
    def eco(self):
        return False if self.sender else True

    def unit_send(self):
        module = import_module(settings.SMS_GATEWAY)
        gateway = module.Gateway()

        try:
            self.sms_id = gateway.send_sms(self)
        except SmsError:
            self.status = 'error'
        else:
            self.date_sent = datetime.now()
            self.status = 'sent'
        self.save()

    @classmethod
    def send(cls):
        toSend = cls.toSend.all()

        for sms in toSend:
            sms.unit_send()
    
    class Meta:
        app_label = "sms"
        verbose_name = _("Sms")
        verbose_name_plural = _("Smses")
        ordering = ['-date_created']
        
    
