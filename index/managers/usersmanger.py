from collections import Counter
from functools import reduce

from ..models.users import User, USER_STATES
from ..models.solutions import Solution
from ..models.houses import House
from .playerutils import Subject, Player, get_rank

def get_all_players(state: str) -> list:
    if state not in USER_STATES:
        return []

    players = []
    for user in User.objects.filter(state=USER_STATES[state]):
        players.append(dox_user(user))
    return sorted(players, key=lambda p: p.total, reverse=True)

def dox_user(user: User):
    total, subjects = get_top_three(Solution.objects.filter(user=user))
    return Player(
        user.nick,
        user.note,
        get_rank(total // 10),
        subjects[0],
        subjects[1],
        subjects[2],
        user.houses.all(),
        total,
        user.image
    )

def get_top_three(solutions: Solution) -> (int, list):
    categories = Counter()
    for sol in solutions:
        categories[sol.challenge.category.name] += sol.get_score()

    return  reduce(lambda val, tup: tup[1] + val, categories.most_common(3), 0), \
            [Subject(name, score) for name, score in (categories.most_common(3) + [('Null', 0)] * 3)]

def add_user(nick: str, state: str, houses: list = [], note: str = "", mail: str = "user@example.com", security: bool = False, ninja: bool = False) -> None:
    user = User(nick=nick, state=state, note=note, mail=mail, security=security, ninja=ninja)
    user.save()
    for house in houses:
        house_decleration = house[0].upper() + house[1:].lower()
        user.houses.add(House.objects.get(name=house_decleration))
