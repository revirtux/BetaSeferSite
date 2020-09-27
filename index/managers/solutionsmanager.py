from ..models.solutions import Solution
from ..models.challenges import Challenge
from ..models.categories import Category
from ..models.users import User


def update_solution(user: str, challenge: str, category: str, multipoint: int = 1):
    if not Category.objects.filter(name=category).exists():
        raise Exception(f"update_solution: Category '{category}' not exists!")

    category_obj = Category.objects.get(name=category)

    if not Challenge.objects.filter(name=challenge, category=category_obj).exists():
        raise Exception(f"update_solution: Challange '{challenge}' at {category} not exists!")

    if not User.objects.filter(nick=user).exists():
        raise Exception(f"update_solution: User '{user}' in {challenge} at {category} not exists!")

    user_obj = User.objects.get(nick=user)

    chall = Challenge.objects.get(name=challenge, category=category_obj)
    if Solution.objects.filter(user=user_obj, challenge=chall).exists():
        solution = Solution.objects.get(user=user_obj, challenge=chall)
        solution.multipoint = multipoint
        solution.save()
    else:
        solution = Solution(user=user_obj, challenge=chall,
                            multipoint=multipoint)
        solution.save()
