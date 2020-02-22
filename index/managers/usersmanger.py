from collections import Counter
from functools import reduce

from ..models.users import User, USER_STATES
from ..models.solutions import Solution
from .playerutils import Subject, Player, get_rank

def get_all_players() -> list:
    players = []
    for user in User.objects.filter(state=USER_STATES['Player']):
        players.append(dox_user(user))
    return sorted(players, key=lambda p: p.total, reverse=True)

def dox_user(user: User):
    total, subjects = get_top_three(Solution.objects.filter(user=user))
    return Player(
        user.nick,
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
        categories[sol.challenge.category.name] += sol.challenge.score

    return  reduce(lambda val, tup: tup[1] + val, categories.most_common(3), 0), \
            [Subject(name, score) for name, score in (categories.most_common(3) + [('Null', 0)] * 3)]
