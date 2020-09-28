from django.db import models
from django.db.models import CharField, BooleanField, ForeignKey, ImageField

class House(models.Model):
    name = models.CharField(max_length=20, default="Untitled")
    motto = models.CharField(max_length=256)
    image = ImageField(upload_to="houses", blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
