from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sms/', include('sms.urls')),

    url(r'^', include(admin.site.urls)),
)
