from django.http import HttpResponse
from django.template import loader
from .managers import usersmanger, housesmanager, common

def cleardb(request):
    common.cleardb()
    return HttpResponse("Done")

def initdb(request):
    common.initdb()
    return HttpResponse("Done")

def init_houses(request):
    common.init_houses()
    return HttpResponse("Done")

def index(request):
    template = loader.get_template('index.html')
    players = usersmanger.get_all_players()
    houses = housesmanager.get_all_houses()
    return HttpResponse(template.render({'players': enumerate(players, 1), 'houses': houses}, request))
