from ..models.games import Game, GameRank
from ..models.users import User, USER_STATES
from ..models.categories import Category
from .usersmanger import get_score_table, get_category_scores
from .playerutils import Player, get_rank
from ..models.solutions import Solution

def get_game_table(game: Game):
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
    pass

def get_managers(game: Game):
    return game.managers.all()