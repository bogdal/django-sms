from django.conf.urls import patterns, include, url
from django.contrib import admin
from smsproject.app.views import HomeView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    # callbacks
    url(r'^sms/', include('sms.urls')),

    # example view
    url(r'', HomeView.as_view(), name='home')
)
