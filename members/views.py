from django.shortcuts import render
from django.views.generic import DetailView, ListView, FormView, TemplateView
from members.models import Member, Group


class MemberDetail(DetailView):
    model = Member


class MemberList(ListView):
    model = Member


class GroupDetail(DetailView):
    model = Group


class GroupList(ListView):
    model = Group


class GClefList(TemplateView):
    template_name = 'members/g_clef_list.html'

    def get_context_data(self, **kwargs):
        context = super(GClefList, self).get_context_data(**kwargs)
        ms = []
        for m in Member.objects.filter(is_pang=False):
            days = m.get_total_membership_time().days
            if days > 365*2.5:
                m.days = days
                m.semesters = days//(365//2)
                ms.append(m)
        context['member_list'] = ms
        return context