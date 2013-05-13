from django.conf.urls import patterns, url
from pages import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^info$', views.info, name='info'),
    url(r'^kontakt$', views.contact, name='contact'),
    url(r'^grupperinger/(?P<group>[\w\-]+)/$', views.group, name='group'),
)
