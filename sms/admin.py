from django.contrib import admin
from django.utils.translation import ugettext as _
from sms.models import Sms, Sender, Inbox


class SmsAdmin(admin.ModelAdmin):
    search_fields = ['recipient', 'content', 'sms_id']
    list_display = ('recipient', 'sender_field', 'status', 'updated', 'content', 'sms_id')
    readonly_fields = ('status', 'sms_id')
    list_filter = ('test', 'sender', 'status', 'recipient')
    actions = ['send_sms']

    fieldsets = [
        (None, {
            'fields': ['recipient', 'content', 'sender'],
        }),
        (_('Advanced'), {
            'fields': ['flash', 'secure', 'test'],
        }),
        (_("State"), {
            'fields': ['status', 'sms_id']
        }),
    ]

    def sender_field(self, obj):
        return obj.sender if obj.sender else "-- eco --"
    sender_field.short_description = _("Sender")

    def send_sms(self, request, queryset):
        counter = 0
        for sms in queryset:
            if sms.send():
                counter += 1
        self.message_user(request, _("Sent messages (%s)" % counter))
    send_sms.short_description = _("Send sms")


class SenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)


class InboxAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'sent', 'parent_content_field')
    
    def parent_content_field(self, obj):
        if obj.parent_sms is not None:
            return obj.parent_sms.content
    parent_content_field.short_description = _("Content of parent sms")


admin.site.register(Sms, SmsAdmin)
admin.site.register(Sender, SenderAdmin)
admin.site.register(Inbox, InboxAdmin)
