from django import forms
from django.contrib import admin
from django.core.urlresolvers import get_resolver
from django.utils.functional import lazy
from dashboard.models import Menu, MenuItem


def move_up(modeladmin, request, queryset):
    for item in queryset.order_by('-position'):
        item.position += 1
        item.save()


def move_down(modeladmin, request, queryset):
    for item in queryset.order_by('position'):
        item.position -= 1
        item.save()


def get_urls(url_list=None, namespace=""):
    if url_list is None:
        url_list = get_resolver('bull.urls').url_patterns
    results = []
    for entry in url_list:
        if hasattr(entry, 'name') and entry.name is None:
            continue
        if hasattr(entry, 'namespace') and entry.namespace == 'admin':
            continue
        if hasattr(entry, 'url_patterns'):
            results += get_urls(entry.url_patterns, namespace + str(entry.namespace or ""))
        else:
            if entry.regex.groups == 0:
                s = (namespace + (":" if namespace else "") + "{}".format(entry.name))
                results.append(s)
    return results


def url_help_text():
    return "Django URLer: " + ", ".join(
        ["<a href=\"javascript:setDjangoUrl('{0}');\">{0}</a>".format(url)
         for url in get_urls()])


class MenuItemAdminForm(forms.ModelForm):
    class Meta:
        help_texts = {
            'url': url_help_text,
        }


class MenuItemAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/admin.js',)
    list_display = ['text', 'parent_menu', 'position', 'sub_menu']
    actions = [move_up, move_down]
    form = MenuItemAdminForm


admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)