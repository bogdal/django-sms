from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from sms.forms import SimpleSmsForm


class HomeView(FormView):
    template_name = 'home.html'
    form_class = SimpleSmsForm

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse("home"))
