from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group as DjangoGroup
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.response import TemplateResponse
from members.forms import BulkAddForm
from members.models import Member, Group, GroupMembership, Position, LoA


class MemberAdmin(UserAdmin):
    bulk_add_template = 'admin/members/member/bulk_add.html'

    bulk_add_form = BulkAddForm

    def get_urls(self):
        urls = super(MemberAdmin, self).get_urls()
        return [
            url(r'^bulk-add/$', self.admin_site.admin_view(self.bulk_add), name='add_bulk')
        ] + urls

    def bulk_add(self, request, form_url=''):
        if not self.has_add_permission(request):
            raise PermissionDenied
        if request.method == 'POST':
            form = self.bulk_add_form(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('..')
        else:
            form = self.bulk_add_form()

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': "Legg til mange brukere",
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'add': True,
            'change': False,
            'opts': self.model._meta,
            'save_as': False,
            'show_save': True,
        }
        context.update(admin.site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(request, self.bulk_add_template, context)

    filter_horizontal = []
    list_filter = []
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personlig info', {'fields': ('first_name', 'last_name', 'birth_date', 'profile_photo', 'is_pang')}),
        ('Kontaktinfo', {'fields': ('postal_code', 'city', 'address', 'phone', 'email')}),
        ('Tilganger', {'fields': ('is_active', 'is_admin')}),
    )
    list_display = ('username', 'first_name', 'last_name')

admin.site.unregister(DjangoGroup)
admin.site.register(Group)
admin.site.register(GroupMembership)
admin.site.register(Position)
admin.site.register(LoA)
admin.site.register(Member, MemberAdmin)