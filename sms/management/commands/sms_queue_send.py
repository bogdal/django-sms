from django.core.management.base import NoArgsCommand
from django.conf import settings
from sms.models import SmsQueue

class Command(NoArgsCommand):
    help = "Send messages from queue"

    def handle_noargs(self, **options):
        SmsQueue.send()
