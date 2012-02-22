 # -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

class SmsSender(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Sender name"), unique=True)
    is_active = models.BooleanField(verbose_name=_("Is active?"), default=True)
    
    def __unicode__(self):
        return self.name
    
    @classmethod
    def synchronize(cls):
        module = import_module(settings.SMS_GATEWAY)
        gateway = module.Gateway()

        senders = gateway.get_senders_list()

        for sender in senders:
            ss, created = cls.objects.get_or_create(name=sender)
            ss.active = True
            ss.save()

        cls.all().exclude(name__in=senders).update(active=False)
            
    
    class Meta:
        app_label = "sms"
        verbose_name = _("Sender")
        verbose_name_plural = _("Senders")
        ordering = ['-name']
        
    
