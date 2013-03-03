from django.db import models

class Page(models.Model):
	pageName = models.CharField(max_length = 1000)
	descriptionText = models.TextField()

# Create your models here.
