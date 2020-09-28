from ..models.users import User
from ..models.categories import Category
from ..models.challenges import Challenge


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

def get_all_challenges(category: Category):
    return Challenge.objects.filter(category__name=Category.name)

