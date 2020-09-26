from ..models.users import User
from ..models.categories import Category
from ..models.challenges import Challenge


def update_challenge(name: str, category: str, description: str = "", score: int = 1, deadline: str = ""):
    if not Category.objects.filter(name=category).exists():
        raise Exception("update_challenge: invalid category")

    category_obj = Category.objects.get(name=category)

    if Challenge.objects.filter(name=name, category=category_obj).exists():
        chall = Challenge.objects.get(name=name, category=category_obj)
        chall.name = name
        chall.category = category_obj
        chall.description = description
        chall.score = score
        chall.deadline = deadline
        chall.save()
    else:
        chall = Challenge(name=name, category=category_obj,
                          description=description, score=score, deadline=deadline)
        chall.save()


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
