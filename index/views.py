from django.http import HttpResponse
from django.template import loader
from .managers import usersmanger, housesmanager, common
from .scripts.scrap import scrap_users

def cleardb(request):
    common.cleardb()
    return HttpResponse("Done")

def initdb(request):
    common.initdb()
    return HttpResponse("Done")

def init_houses(request):
    common.init_houses()
    return HttpResponse("Done")

def load_file(request):
    players = ""
    return HttpResponse(players)

def index(request):
    template = loader.get_template('index.html')
    players = usersmanger.get_all_players('Player')
    zombies = usersmanger.get_all_players('Zombie')
    pensioners = usersmanger.get_all_players('Pensioner')
    commemorations = usersmanger.get_all_players('Commemoration')
    houses = housesmanager.get_all_houses()
    return HttpResponse(template.render(
        {
            'players': enumerate(players, 1),
            'zombies': enumerate(zombies, 1),
            'pensioners': enumerate(pensioners, 1),
            'commemorations': enumerate(commemorations, 1),
            'houses': houses
        }, request))

def scrap(request):
    scrap_users()
    return HttpResponse("Done")