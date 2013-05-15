from django.db import models
from tinymce import models as tinymce_models
from tinymce.widgets import TinyMCE
from snippets.unique_slugify import unique_slugify


class Category(models.Model):
    category_name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.category_name


class Page(models.Model):
    page_name = models.CharField(max_length=1000)
    slug = models.SlugField(editable=False)
    category = models.ForeignKey(Category)
    description_text = tinymce_models.HTMLField()

    def save(self, **kwargs):
        slug = '%s' % self.page_name
        unique_slugify(self, slug)
        super(Page, self).save()

    def __unicode__(self):
        return self.page_name