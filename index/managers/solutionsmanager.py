from ..models.solutions import Solution


def update_solution(user: str, challenge: str, multipoint: int = 1):
    if Solution.objects.filter(user=user, challenge=challenge).exists():
        solution = Solution.objects.get(user=user, challenge=challenge)
        solution.multipoint = multipoint
        solution.save()
    else:
        solution = Solution(user=user, challenge=challenge,
                            multipoint=multipoint)
        solution.save()
