from django.conf.urls.defaults import patterns, include, url
from pages import views

urlpatterns = patterns('',
    url(r'^$', views.pages, name='pages'),
)
