from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView
from members.models import Member, Group


class MemberDetail(DetailView):
    model = Member


class MemberList(ListView):
    model = Member


class GroupDetail(DetailView):
    model = Group


class GroupList(ListView):
    model = Group


class MemberBulkAdd(FormView):
    pass