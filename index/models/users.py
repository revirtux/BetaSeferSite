from django.db import models
from django.db.models import CharField, BooleanField, ForeignKey, ManyToManyField, ImageField

from .houses import House

USER_STATES = {
    'Player':'G',
    'Pensioner':'P',
    'Zombie':'Z',
    'Commemoration':'C',
    'Testing': 'T'
}

class User(models.Model):
    nick = CharField(max_length=30)
    note = CharField(max_length=256, default="")
    mail = CharField(max_length=100, default="user@example.com")
    security = BooleanField(default=False)
    ninja = BooleanField(default=False)
    houses = ManyToManyField(House, null=False)
    state = CharField(max_length=1, choices=[(b, a) for a, b in USER_STATES.items()], default=USER_STATES['Player'])
    image = ImageField(upload_to="users", blank=True, null=True)

    def __str__(self):
        return f"{self.nick}"
