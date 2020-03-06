from dataclasses import dataclass
from django.db.models import ImageField

@dataclass
class Rank:
    level: str
    color: str

@dataclass
class Subject:
    name: str
    score: int

@dataclass
class Player:
    nick: str
    note: str
    rank: Rank
    first: Subject
    sec1: Subject
    sec2: Subject
    houses: str
    total: int
    image: ImageField

def get_rank(score):
    if score <= 1:
        return Rank(str(score), 'white')
    elif score <= 4:
        return Rank(str(score), 'yellow')
    elif score <= 7:
        return Rank(str(score), 'orange')
    elif score <= 10:
        return Rank(str(score), 'green')
    elif score <= 13:
        return Rank(str(score), 'blue')
    elif score <= 16:
        return Rank(str(score), 'puple')
    elif score <= 19:
        return Rank(str(score), 'brown')
    else:
        return Rank('ninja', 'ninja')
