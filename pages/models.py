from django.db import models


class Category(models.Model):
    category_name = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.category_name


class Page(models.Model):
    page_name = models.CharField(max_length=1000)
    category = models.ForeignKey(Category)
    description_text = models.TextField()

    def __unicode__(self):
        return self.page_name