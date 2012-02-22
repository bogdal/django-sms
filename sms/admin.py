# -*- coding: utf-8 -*
from django.contrib import admin
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from sms.models import SmsQueue, SmsSender, SmsReceive

class SmsQueueAdmin(admin.ModelAdmin):
    search_fields = ['recipient', 'content','sms_id']
    list_display = ('recipient','sender_field', 'status', 'content', 'date_sent','sms_id')
    list_filter = ('test', 'sender')
    actions = ['send_sms']

    def sender_field(self, obj):
        return obj.sender if obj.sender else "-- eco --"
    sender_field.short_description = _("Sender")

    def send_sms(self, request, queryset):
        for sms in queryset:
            if sms.status == 'not_sent':
                sms.unit_send()
        self.message_user(request, _("Sms sent"))
    send_sms.short_description = _("Send sms")


class SmsSenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')

class SmsReceiveAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'date_sent')

admin.site.register(SmsQueue, SmsQueueAdmin)
admin.site.register(SmsSender, SmsSenderAdmin)
admin.site.register(SmsReceive, SmsReceiveAdmin)
