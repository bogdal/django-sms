from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.utils.translation import ugettext as _
from sms.forms import SimpleSmsForm


class HomeView(FormView):
    template_name = 'app/home.html'
    form_class = SimpleSmsForm

    def form_valid(self, form):
        # form.save()
        messages.success(self.request, _("Message was sent"))
        return HttpResponseRedirect(reverse("home"))
