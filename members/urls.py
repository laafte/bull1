from django.conf.urls import url
from members.views import MemberDetail, MemberList, GroupDetail, GroupList, GClefList

urlpatterns = [
    url(r'^grupper/$', GroupList.as_view(), name='groups'),
    url(r'^grupper/(?P<pk>\d*)', GroupDetail.as_view(), name='group'),
    url(r'^medlemmer/$', MemberList.as_view(), name='members'),
    url(r'^medlemmer/panger/nye/$', GClefList.as_view(), name='new_pangs'),
    url(r'^medlemmer/(?P<pk>\d*)/$', MemberDetail.as_view(), name='member'),
]