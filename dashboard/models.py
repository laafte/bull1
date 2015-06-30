from django.core.urlresolvers import reverse, get_resolver
from django.db import models
from django.utils.functional import lazy


class Menu(models.Model):
    """
    A menu shown on the dashboard interface
    """
    class Meta:
        verbose_name = "Meny"
        verbose_name_plural = "Menyer"

    SIDEBAR = 1
    TOP = 2
    MENU_SLOTS = (
        (SIDEBAR, 'Sidebar'),
        (TOP, 'Topp'),
    )

    name = models.CharField(max_length=50, verbose_name="navn")
    slot = models.IntegerField(choices=MENU_SLOTS, blank=True, null=True, unique=True, verbose_name="plassering")

    def clean(self):
        pass

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """
    An item in a menu.
    """
    class Meta:
        verbose_name = "Menyelement"
        verbose_name_plural = "Menyelementer"
        ordering = ['parent_menu', 'position']
        unique_together = ['position', 'parent_menu']

    text = models.CharField(max_length=50, verbose_name="tekst")
    icon = models.CharField(max_length=50, verbose_name="ikon",
                            help_text="<a href=\"https://www.google.com/design/icons/\">Oversikt over ikoner</a>", blank=True)
    url = models.CharField(max_length=255, verbose_name="URL")
    url_is_django = models.BooleanField(verbose_name="URL er django-url-navn", default=False,
                                        help_text="Ikke huk av denne om du ikke forstår hva det vil si.")
    parent_menu = models.ForeignKey(Menu, verbose_name="i meny", related_name='items')
    sub_menu = models.OneToOneField(Menu, verbose_name="inneholder meny",
                                    related_name='parent_item', blank=True, null=True)
    position = models.IntegerField(verbose_name="posisjon")

    def real_url(self):
        if self.url_is_django:
            return reverse(self.url)
        return self.url

    def clean(self):
        pass

    def __str__(self):
        return "{} ({})".format(self.text, self.parent_menu)
