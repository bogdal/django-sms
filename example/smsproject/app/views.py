from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.utils.translation import ugettext as _
from smsproject.app.forms import SimpleSmsForm


class HomeView(FormView):
    template_name = 'app/home.html'
    form_class = SimpleSmsForm

    def get_initial(self):
        initial = {
            'sender': self.request.session.get('sender'),
            'recipient': "+48",
        }
        return initial

    def form_valid(self, form):
        form.save()
        self.request.session['sender'] = form.cleaned_data.get('sender')
        messages.success(self.request, _("Message was sent"))
        return HttpResponseRedirect(reverse("home"))
