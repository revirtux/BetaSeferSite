from django.db import models
from django.db.models import CharField, ForeignKey, ImageField, IntegerField, ManyToManyField, OneToOneField

from .categories import Category
from .users import User

class GameRank(models.Model):
    name = CharField(max_length=64)
    badge = ImageField(upload_to="game_badges", blank=True, null=True)
    min_place = IntegerField(default=1)

    def __str__(self):
        return f"{self.name}"

class Game(models.Model):
    category = OneToOneField(Category, on_delete=models.CASCADE, default=None)
    name = CharField(max_length=64)
    getting_points_desc = CharField(max_length=2048)
    leveling_desc = CharField(max_length=2048)
    managers = ManyToManyField(User, null=False)
    ranks = ManyToManyField(GameRank, null=False)

    def __str__(self):
        return f"Game of {self.name}"
