from django.core.management.base import NoArgsCommand
from sms.models import Sender


class Command(NoArgsCommand):
    help = "Synchronize Gateway Senders"

    def handle_noargs(self, **options):
        Sender.synchronize()

        print 'Done'