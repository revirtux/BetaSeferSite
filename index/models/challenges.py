from django.db import models
from django.db.models import CharField, IntegerField, ForeignKey

from .categories import Category

class Challenge(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=256)
    score = IntegerField(default=1)
    category = ForeignKey(Category, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.name}"
