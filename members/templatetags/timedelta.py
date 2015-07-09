from django import template

register = template.Library()


@register.filter
def time_delta(value, arg="%D dager"):
    """
    Prints a timedelta in human readable format, optionally according to a
    format string
    """
    d = value.days
    h = value.seconds//3600 if '%H' in arg else 0
    m = (value.seconds - (h*3600))//60 if "%M" in arg else 0
    s = value.seconds - (h*3600) - (m*60)
    return arg.replace("%D", str(d)).replace("%H", str(h)).replace("%M", str(m)).replace("%S", str(s))