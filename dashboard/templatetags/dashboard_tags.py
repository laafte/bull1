from django import template
from django.template import Context
from django.template.loader import get_template
from dashboard.models import Menu

register = template.Library()


@register.simple_tag
def icon(name, *args, **kwargs):
    extra_classes = kwargs.get('extra_classes', '')
    size = kwargs.get('size', '')
    if size == 'small':
        extra_classes = "small " + extra_classes
    return '<span class="material-icons {}">{}</span>'.format(extra_classes, name)


@register.simple_tag(takes_context=True)
def active_class(context, menu_item):
    url = menu_item.real_url()
    path = context['request'].path
    active = (path == url) if (url == "/") else (path.startswith(url))
    return ' class = "active"' if active else ""


def _load_menu(slot):
    try:
        return Menu.objects.get(slot=slot)
    except Menu.DoesNotExist:
        return []


@register.simple_tag(takes_context=True)
def menu(context, slot, *args, **kwargs):
    if slot == "sidebar":
        menu_ = _load_menu(Menu.SIDEBAR)
        return get_template("sidebar.html").render(Context({
            'menu': menu_,
            'request': context['request'],
        }))
    elif slot == "top":
        menu_ = _load_menu(Menu.TOP)
        return get_template("top_menu.html").render(Context({
            'menu': menu_,
            'request': context['request'],
        }))