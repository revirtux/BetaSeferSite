from ..models.houses import House

def get_all_houses():
    return House.objects.all()