from ..models.categories import Category
from ..models.houses import House
from ..models.challenges import Challenge
from ..models.users import User
from ..models.solutions import Solution

def cleardb():
    objects = list(User.objects.all()) + \
            list(Challenge.objects.all()) + \
            list(Solution.objects.all()) + \
            list(Category.objects.all())
    for obj in objects:
        obj.delete()

def initdb():
    user = User(nick="user")
    user.save()
    user.houses.add(House.objects.filter(name="Dworkin")[0])
    category = Category(name="General", description="cyber?", manager=user)
    category.save()
    chall = Challenge(name="chall", description="desc", category=category)
    chall.save()
    sol = Solution(user=user, challenge=chall)
    sol.save()


def init_houses():
    for house_name in ('Mallory', 'Pie', 'Gopher', 'Vector', 'Dworkin', 'Gene', 'Greenhouse'):
        house = House(name=house_name, moto="this")
        house.save()