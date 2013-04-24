from django import forms
from sms import forms as sms_forms


class SimpleSmsForm(sms_forms.SimpleSmsForm):

    class Meta(sms_forms.SimpleSmsForm.Meta):
        widgets = {
            'sender': forms.TextInput(attrs={'placeholder': "e.g. John"}),
            'recipient': forms.TextInput(attrs={'placeholder': "e.g. +48111222333"}),
        }
