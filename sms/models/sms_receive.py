 # -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext as _
from datetime import date, datetime

class SmsReceive(models.Model):
    sender = models.CharField(max_length=11, verbose_name=_("Sender"))
    recipient = models.CharField(max_length=11, verbose_name=_("Recipient"))
    content = models.TextField(verbose_name=_("Message content"), blank=True, null=True)
    date_sent = models.DateTimeField(verbose_name=_("Date sent"), blank=True, null=True)
    date_created = models.DateTimeField(verbose_name=_("Date created"), auto_now_add=True)
    parent_sms = models.ForeignKey('SmsQueue', verbose_name=_("Parent sms"), blank=True, null=True)
    
    objects = models.Manager()
    
    def __unicode__(self):
        return self.sender

    class Meta:
        app_label = "sms"
        verbose_name = _("Receive sms")
        verbose_name_plural = _("Receive smses")
        ordering = ['-date_sent']
        
    
