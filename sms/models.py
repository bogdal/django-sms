from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext as _
from sms import SmsError
from sms.gateway.sms_gateway import SmsGateway
from sms.signals import post_send_sms
from phonenumber_field.modelfields import PhoneNumberField


class AbstractSms(models.Model):
    sender = models.CharField(max_length=12, blank=True, null=True, verbose_name=_('sender'))
    recipient = PhoneNumberField()
    content = models.TextField(verbose_name=_('content'))

    class Meta:
        abstract = True


class Sender(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('name'), unique=True)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def synchronize(cls):
        gateway = SmsGateway()
        senders = gateway.get_senders()

        for sender in senders:
            ss, created = cls.objects.get_or_create(name=sender)
            ss.active = True
            ss.save()

        cls.objects.all().exclude(name__in=senders).update(is_active=False)

    class Meta:
        app_label = 'sms'
        verbose_name = _('Sender')
        verbose_name_plural = _('Senders')
        ordering = ['-name']


class Sms(AbstractSms):

    NEW = 'new'
    SENT = 'sent'
    ERROR = 'error'
    DELIVERED = 'delivered'
    NOT_DELIVERED = 'not_delivered'

    SMS_STATUSES = (
        (NEW, _('New')),
        (SENT, _('Sent')),
        (ERROR, _('Dispatch error')),
        (DELIVERED, _('Delivered')),
        (NOT_DELIVERED, _('Not delivered')),
    )

    flash = models.BooleanField(verbose_name=_('flash'), default=False)
    secure = models.BooleanField(verbose_name=_('secure'), default=False,
                                 help_text=_('Sms content after sending will be removed'))
    created = models.DateTimeField(_('created'), auto_now_add=True)
    updated = models.DateTimeField(_('updated'), auto_now=True)
    status = models.CharField(max_length=50, choices=SMS_STATUSES, default=NEW, verbose_name=_('status'))
    sms_id = models.CharField(max_length=50, verbose_name=_('provider ID'), blank=True, null=True)
    test = models.BooleanField(verbose_name=_('test'), default=False)
    is_active = models.BooleanField(verbose_name=_('is active'), default=True)

    def __unicode__(self):
        return unicode(self.recipient)

    class Meta:
        verbose_name = _('Sms')
        verbose_name_plural = _('Smses')
        ordering = ['-created']

    @property
    def eco(self):
        return self.sender is None

    def send(self):
        sms_id = None
        if self.status in [self.NEW, self.ERROR]:
            gateway = SmsGateway()
            try:
                sms_id = gateway.send_sms(self)
            except SmsError:
                self.status = self.ERROR
            else:
                self.status = self.SENT
                self.sms_id = sms_id
                if self.secure:
                    self.content = _('secure sms')
            self.save()
            post_send_sms.send(sender=Sms, sms=self)
        return sms_id


class Inbox(AbstractSms):
    created = models.DateTimeField(_('created'), auto_now_add=True)
    sent = models.DateTimeField(verbose_name=_('sent'), blank=True, null=True)
    parent_sms = models.ForeignKey('sms.Sms', verbose_name=_('parent'), blank=True, null=True)

    def __unicode__(self):
        return self.sender

    class Meta:
        verbose_name = _('Inbox')
        verbose_name_plural = _('Inbox')
        ordering = ['-sent']


@receiver(post_save, sender=Sms)
def send_sms(sender, **kwargs):
    if kwargs.get('created'):
        kwargs.get('instance').send()
