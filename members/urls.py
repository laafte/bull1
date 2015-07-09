from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView, DetailView, RedirectView
from members.models import Group
from members.views import GClefList, gclef_pdf, MemberList, ProfileView, ProfileEditView, ProfileCreateView

urlpatterns = [
    url(r'^medlemmer/grupper/$', ListView.as_view(model=Group), name='groups'),
    url(r'^medlemmer/grupper/(?P<pk>\d*)', DetailView.as_view(model=Group), name='group'),
    url(r'^medlemmer/$', RedirectView.as_view(url=reverse_lazy('members:active')), name='members'),
    url(r'^medlemmer/aktive/$', MemberList.as_view(), name='active'),
    url(r'^medlemmer/panger/nye/$', GClefList.as_view(), name='pangs'),
    url(r'^medlemmer/panger/nye/rapport.pdf$', gclef_pdf, name='pangs_pdf'),
    url(r'^medlemmer/(?P<pk>\d*)/$', ProfileView.as_view(), name='member'),
    url(r'^medlemmer/rediger-profil/$', ProfileEditView.as_view(), name='edit_profile'),
    url(r'^medlemmer/registrer-profil/$', ProfileCreateView.as_view(), name='create_profile'),
]