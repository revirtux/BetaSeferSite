from django.db import models
from django.db.models import CharField, BooleanField, ForeignKey

from .users import User

class Category(models.Model):
    name = CharField(max_length=20)
    description = CharField(max_length=256)
    manager = ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
