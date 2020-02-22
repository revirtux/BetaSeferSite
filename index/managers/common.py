from ..models.categories import Category
from ..models.houses import House
from ..models.challenges import Challenge
from ..models.users import User
from ..models.solutions import Solution

def cleardb():
    objects = list(User.objects.all()) + \
            list(Challenge.objects.all()) + \
            list(Solution.objects.all()) + \
            list(Category.objects.all()) + \
            list(House.objects.all())

    for obj in objects:
        obj.delete()

def initdb():
    for house_name in ('Malory', 'Pie', 'Gopher', 'Vector', 'Dworkin'):
        house = House(name=house_name)
        house.save()
        
    user = User(nick="user")
    user.save()
    category = Category(name="General", description="cyber?", manager=user)
    category.save()
    chall = Challenge(name="chall", description="desc", category=category)
    chall.save()
    sol = Solution(user=user, challenge=chall)
    sol.save()
