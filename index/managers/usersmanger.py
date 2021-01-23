from collections import Counter
from functools import reduce

from ..models.users import User, USER_STATES
from ..models.solutions import Solution
from ..models.houses import House
from ..models.categories import Category
from ..models.games import Game
from .playerutils import Subject, Player, get_rank
from .housesmanager import get_houses_name, get_all_houses
from .gamesmanager import get_badges
from .categoriesmanager import get_all_categories, get_category_object
from django.db.models.query import prefetch_related_objects

"""
Used by the function ./views.py/profile
TODO: Add a function to dox a user without a user object (@AmitTPB)
"""
def get_user_by_nick(nick):
    return User.objects.filter(nick=nick).first()


def get_score_table(state: str = "", house: str = ""):
    """
    Returns a table with the score of every player in every category.

    :param state: Only return players in this state
    :param house: Only return players in this house
    :return: A dictionary with keys as User objects and values as more dictionaries of Category objects and their values
        are the score of the user in the category.
    """
    if state and state not in USER_STATES:
        return []
    if house and house not in get_houses_name():
        return []
    
    solutions = Solution.objects.select_related("user").select_related("challenge__category")
    
    if state:
        solutions = solutions.filter(user__state=USER_STATES[state])
    if house:
        solutions = solutions.filter(user__houses__name=house)
        
    
    d = dict()

    for sol in solutions:
        user = sol.user
        category = sol.challenge.category
        if user not in d:
            d[user] = dict()
        d[user][category] = d[user].get(category, 0) + sol.get_score()
    
    return d

def new_get_top_three(scores: dict) -> list:
    """
    Returns the top 3 subjects and their score as a Subject object.

    :param scores: A scores dictionary where the keys are categories and the values are scores
    :return: The top 3 Subject objects in an array
    """
    return [Subject(name, score) for name, score in (
            Counter(scores).most_common(3) + [('Null', 0)] * 3)]

def get_main_table(state: str = "", house: str = ""):
    """
    Gets a scores table of sorted Player objects which can be filtered by house and state.

    :param state: A state filter
    :param house: A house filter
    :return: Scores table as an array of Player objects.
    """
    players = User.objects.prefetch_related("houses")

    score_table = get_score_table(state, house)
    users = []
    badges = dict()

    for game in Game.objects.all():
        game_badges = get_badges(game)
        for user in game_badges:
            badges[user] = badges.get(user, []) + game_badges[user]

    for player in players:
        if player not in score_table:
            continue
        chal_dict = score_table[player]
        total = sum(chal_dict.values())
        subjects = new_get_top_three(chal_dict)
        users.append(Player(
            player.nick,
            player.note,
            get_rank(total // 10),
            subjects[0],
            subjects[1],
            subjects[2],
            player.houses.all(),
            total,
            player.image,
            badges.get(player.nick, [])
        ))

    return sorted(users, key=lambda p: p.total, reverse=True)


def dox_user(user: User) -> Player:
    """
    Returns data about a User object in a Player object.
    Not recommended for use because of performance issues.

    :param user: A user object
    :return: A corresponding Player object.
    """
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
        user.image,
        []
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
