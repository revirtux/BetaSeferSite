from ..models.games import Game, GameRank
from ..models.users import User
from ..models.solutions import Solution
from .usersmanger import get_category_score



def get_game_data(game: Game):
    # TODO: Rewrite after caching work


def get_managers(game: Game):
    return game.managers.all()