from django.conf.urls import url
from django.views.generic import DetailView
from members.views import MemberDetail, MemberList, GroupDetail, GroupList, MemberBulkAdd

urlpatterns = [
    url(r'^grupper/$', GroupList.as_view()),
    url(r'^grupper/(?P<pk>\d*)', GroupDetail.as_view()),
    url(r'^medlemmer/$', MemberList.as_view()),
    url(r'^medlemmer/(?P<pk>\d*)', MemberDetail.as_view()),
]