from django.db import models

from tinymce import models as tinymce_models

# Create your models here.
class Project(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, default="")
    description = tinymce_models.HTMLField()
    technology = models.CharField(max_length=255)
    categories = models.ManyToManyField('Category', related_name='project')
    #images = models.FilePathField(path="/img")

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name