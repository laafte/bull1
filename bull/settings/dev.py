# Load defaults in order to then add/override with dev-only settings
from .common import *

DEBUG = True

STATIC_ROOT = "/home/johan/PycharmProjects/bull/static"

STATICFILES_DIRS = (
    "/home/johan/PycharmProjects/bull/bull/staticfiles",
)

TEMPLATE_DIRS = (
    "/home/johan/PycharmProjects/bull/bull/templates",
)