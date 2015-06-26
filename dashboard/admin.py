from django.contrib import admin
from dashboard.models import Menu, MenuItem


def move_up(modeladmin, request, queryset):
    for item in queryset.order_by('-position'):
        item.position += 1
        item.save()


def move_down(modeladmin, request, queryset):
    for item in queryset.order_by('position'):
        item.position -= 1
        item.save()


class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['text', 'parent_menu', 'position', 'sub_menu']
    actions = [move_up, move_down]

admin.site.register(Menu)
admin.site.register(MenuItem, MenuItemAdmin)