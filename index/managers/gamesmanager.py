from ..models.games import Game, GameRank
from ..models.users import User, USER_STATES
from ..models.categories import Category
from .playerutils import Player, get_rank
from .categoriesmanager import get_category_scores
from ..models.solutions import Solution

def get_game_table(game: Game):
    """
    Returns the table of a given Game object.

    :param game: A given Game object.
    :return: A table of Player objects which represent users in the given game
    """
    badges = sorted(list(game.ranks.all()), key=lambda rank: rank.min_place)
    scores = get_category_scores(game.category)
    users = list(User.objects.filter(state=USER_STATES["player"]))
    users.sort(key=lambda user: scores[user], reverse=True)
    current_badge = 0

    for i in range(len(users)):
        if badges[current_badge].min_place == i and len(badges) > i:
            current_badge += 1
        player = users[i]
        total = scores[player]
        users[i] = Player(
            player.nick,
            player.note,
            get_rank(total // 10),
            None,
            None,
            None,
            None,
            total,
            player.image,
            [badges[current_badge]]
        )
    
    return users


def get_badges(game: Game):
    """
    Returns the the badges of all players in a given game.

    :param game: A given game.
    :return: Returns a dictionary in which the keys are player names and the values are arrays of their Game Ranks whice
        in which they have badges.
    """
    table = get_game_table(game)
    d = dict()

    for player in table:
        if player.ranks[0].badge:
            d[player.nick] = d.get(player.nick, []) + [player.ranks[0]]
    
    return d

def get_managers(game: Game):
    return game.managers.all()
