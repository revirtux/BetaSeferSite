from ..models.users import User
from ..models.categories import Category
from ..models.challenges import Challenge
from ..models.solutions import Solution


def update_category(name: str, description: str = "", manager: str = ""):
    if Category.objects.filter(name=name).exists():
        category = Category.objects.get(name=name)
        category.description = description
        if manager:
            category.manager = User.objects.get(name=manager)
        category.save()
    else:
        category = Category(name=name, description=description)
        if manager:
            category.manager = User.objects.get(name=manager)
        category.save()


def get_all_categories():
    return Category.objects.all()

def get_category_object(name: str=""):
    results = Category.objects.filter(name=name)
    return None if len(results) == 0 else results[0]

def get_all_challenges(category_name: str):
    return Challenge.objects.filter(category__name=category_name)

def get_game(category: Category):
    try:
        return category.game
    except:
        return None

def get_category_scores(category: Category):
    solutions = Solution.objects.filter(challenge__category=category).select_related("user").select_related("challenge")
    d = dict()

    for sol in solutions:
        d[sol.user] = d.get(sol.user, 0) + sol.get_score()
    
    return d
