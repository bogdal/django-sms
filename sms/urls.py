from django.conf.urls.defaults import *

urlpatterns = patterns('sms.views',
    (r'^received_sms/$','callback_received_sms'),
    (r'^delivery_report/$','callback_delivery_report'),
)