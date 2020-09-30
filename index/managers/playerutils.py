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
    houses: list
    total: int
    image: ImageField


def get_rank(score, score_ninjafy=True):
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
        return Rank(str(score), 'purple')
    elif score <= 19:
        return Rank(str(score), 'brown')
    else:
        if score_ninjafy:
            return Rank('ninja', 'ninja')
        else:
            return Rank(str(score), 'ninja')
