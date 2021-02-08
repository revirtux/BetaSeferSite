from django.db import models
from django.db.models import IntegerField, CharField, ForeignKey, ManyToManyField, ImageField

class Page(models.Model):
    title = CharField(max_length=64)

    def __str__(self):
        return f"{self.title}"

class PageText(models.Model):
    header = CharField(max_length=64)
    text = CharField(max_length=2048)
    ordering_id = IntegerField(default=-1)
    Page = models.ForeignKey(Page, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.header}"
