from django.db import models
from django.db.models import IntegerField, CharField, BooleanField, ForeignKey

from .challenges import Challenge
from .users import User

class Solution(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    challenge = ForeignKey(Challenge, on_delete=models.CASCADE)
    multipoint = IntegerField(default=1)
    
    def __add__(self, other):
        if isinstance(other, Solution):
            return self.get_score() + other.get_score()
        elif type(other) in [int, float]:
            return self.get_score() + other
        else:
            raise NotImplementedError()
    
    def __str__(self):
        return f"{self.user.nick} solved {self.challenge.name}"

    def get_score(self):
        return self.challenge.score * self.multipoint