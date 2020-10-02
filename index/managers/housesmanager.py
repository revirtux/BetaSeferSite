from ..models.houses import House


def get_all_houses():
    return House.objects.all()


def get_house(name):
    return House.objects.get(name=name)


def get_houses_name():
    return [house.name for house in get_all_houses()]