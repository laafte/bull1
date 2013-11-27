from django.conf.urls import patterns, url
from bull.pages import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='home'),
    url(r'^info$', views.info, name='info'),
    url(r'^kontakt$', views.contact, name='contact'),
    url(r'^grupperinger/(?P<group>[-\w\d]+)/$', views.group, name='group'),
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
)
