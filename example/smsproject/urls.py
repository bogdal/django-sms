from django.conf.urls import patterns, include, url
from django.contrib import admin
from smsproject.app.views import HomeView
from django.contrib.auth.decorators import login_required

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),

    # sms callbacks
    url(r'^sms/', include('sms.urls')),

    # default view
    url(r'', login_required(HomeView.as_view()), name='home')
)
