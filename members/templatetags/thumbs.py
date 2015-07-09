import os
from django import template
from django.conf import settings

register = template.Library()


def _avatar_hash(user):
    return user.pk % 10


@register.simple_tag
def thumb(user, size):
    """
    Tries to return the URL of the users thumbnail. If one is not found, falls
    back to a 'random' cute kitten
    """
    return user.thumb_url(size) or os.path.join(settings.STATIC_URL, "avatars/s_{}/{}.jpg".format(
        min([s for s in settings.THUMB_SIZES if s >= size]), _avatar_hash(user)))