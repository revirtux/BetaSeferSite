from django.db import models
from django.db.models import CharField, BooleanField, ForeignKey

from .challenges import Challenge
from .users import User

class Solution(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE)
    challenge = ForeignKey(Challenge, on_delete=models.CASCADE)
    
    def __add__(self, other):
        if isinstance(other, Solution):
            return self.challenge.score + other.challenge.score
        elif type(other) in [int, float]:
            return self.challenge.score + other
        else:
            raise NotImplementedError()
    
    def __str__(self):
        return f"{self.user.nick} solved {self.challenge.name}"