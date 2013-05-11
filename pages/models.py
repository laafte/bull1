from django.db import models


class Category(models.Model):
    categoryName = models.CharField(max_length=1000)

    def __unicode__(self):
        return self.categoryName


class Page(models.Model):
    pageName = models.CharField(max_length=1000)
    category = models.ForeignKey(Category)
    descriptionText = models.TextField()

    def __unicode__(self):
        return self.pageName