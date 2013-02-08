import django.dispatch

post_send_sms = django.dispatch.Signal(providing_args=['sms'])