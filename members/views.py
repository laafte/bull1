from datetime import date
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, FormView, RedirectView, UpdateView
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, SimpleDocTemplate, Paragraph, TableStyle, Spacer
from members.forms import GClefForm, ProfileCreateForm
from members.models import Member, Group
from pdf_templates.templates import HeaderFooterDocument


class MemberList(ListView):

    def get_queryset(self):
        return Member.objects.filter(is_active=True)


class ProfileView(DetailView):
    model = Member


class ProfileEditView(UpdateView):
    model = Member
    fields = ['first_name', 'last_name', 'bio', 'email', 'address', 'postal_code', 'city', 'phone', 'profile_photo']
    template_name = 'members/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user


class ProfileCreateView(UpdateView):
    model = Member
    template_name = 'members/create_profile.html'
    form_class = ProfileCreateForm

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return self.request.user.get_absolute_url()

    def dispatch(self, request, *args, **kwargs):
        return super(ProfileCreateView, self).dispatch(request, *args, **kwargs)


class GClefList(FormView):
    template_name = 'members/g_clef_list.html'
    # TODO: Add correct URL here
    success_url = '/'
    form_class = GClefForm

    def form_valid(self, form):
        new_pangs = form.get_new_pangs()
        for p in new_pangs:
            p.is_pang = True
            p.save()
        return super(GClefList, self).form_valid(form)

    def form_invalid(self, form):
        return HttpResponse("Invalid. bound: {}, errors: {}".format(form.is_bound, form.errors))


def gclef_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="gnøkkel-rapport.pdf"'

    doc = HeaderFooterDocument(response, pagesize=A4, leftMargin=cm, rightMargin=cm)

    doc.title = "Oversikt over G-nøkler"

    elements = []

    pangs = Member.get_potential_pangs()
    rows = [("ID", "Navn", "Total medlemstid")]
    rows += [(m.pk, m.get_full_name(), "{} semestre ({} dager)".format(m.semesters, m.days))
             for m in pangs]

    t = Table(rows, hAlign='LEFT', colWidths=(50, '*', 120), repeatRows=1)
    t.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, 0), "Helvetica-Bold"),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), (colors.white,)),
        ('GRID', (0, 0), (-1, -1), 0.1, colors.black),
        ('LINEBELOW', (0, 0), (-1, 0), 1.5, colors.black),
    ]))

    elements.append(t)

    doc.build(elements)

    return response