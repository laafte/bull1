from django.db import models


class Category(models.Model):
    categoryName = models.CharField(max_length=1000)


class Page(models.Model):
    pageName = models.CharField(max_length=1000)
    category = models.ForeignKey(Category)
    descriptionText = models.TextField()


