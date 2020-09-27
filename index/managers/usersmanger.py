from collections import Counter
from functools import reduce

from ..models.users import User, USER_STATES
from ..models.solutions import Solution
from ..models.houses import House
from .playerutils import Subject, Player, get_rank
from .housesmanager import get_houses_name


def get_all_players(state: str = "", house: str = "") -> list:
    if state and state not in USER_STATES:
        return []

    if house and house not in get_houses_name():
        return []

    users = User.objects.all()
    if state:
        users = users.filter(state=USER_STATES[state])
    
    if house:
        users = users.filter(houses__name=house)

    players = []
    for user in users:
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

    return reduce(lambda val, tup: tup[1] + val, categories.most_common(3), 0), \
        [Subject(name, score) for name, score in (
            categories.most_common(3) + [('Null', 0)] * 3)]


def update_user(nick: str, state: str, houses: list = [], note: str = "", mail: str = "user@example.com", security: bool = False, ninja: bool = False) -> None:
    if state not in USER_STATES:
        raise Exception("update_user: invalid state")
    
    if User.objects.filter(nick=nick).exists():
        user = User.objects.get(nick=nick)
        user.state = USER_STATES[state]
        user.note = note
        user.main = mail
        user.security = security
        user.ninja = ninja

        for house in houses:
            user.houses.add(House.objects.get(name=house.title()))
        
        user.save()
    else:
        user = User(nick=nick, state=USER_STATES[state], note=note,
                    mail=mail, security=security, ninja=ninja)

        user.save()

        for house in houses:
            user.houses.add(House.objects.get(name=house.title()))
        
        user.save()
