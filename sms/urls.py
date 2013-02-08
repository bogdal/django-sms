from django.conf.urls import patterns, url
from sms.decorators import ip_restrictions
from sms.views import callback_received_sms, callback_delivery_report

urlpatterns = patterns('sms.views',
    url(r'^callback/received-sms/$', ip_restrictions(callback_received_sms), name='callback-received-sms'),
    url(r'^callback/delivery-report/$', ip_restrictions(callback_delivery_report), name='callback-delivery-report'),
)