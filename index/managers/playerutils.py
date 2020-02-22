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
    rank: Rank
    first: Subject
    sec1: Subject
    sec2: Subject
    houses: str
    total: int
    image: ImageField

def get_rank(score):
    if 1 >= score: 
        return Rank(str(score), 'white')
    elif 4 >= score: 
        return Rank(str(score), 'yellow')
    elif 7 >= score: 
        return Rank(str(score), 'orange')
    elif 10 >= score: 
        return Rank(str(score), 'green')
    elif 13 >= score: 
        return Rank(str(score), 'blue')
    elif 16 >= score: 
        return Rank(str(score), 'puple')
    elif 19 >= score: 
        return Rank(str(score), 'brown')
    else: 
        return Rank('ninja', 'ninja')
