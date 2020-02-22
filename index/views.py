from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .managers import usersmanger, common

def cleardb(request):
    common.cleardb()
    return HttpResponse("Done")

def initdb(request):
    common.initdb()
    return HttpResponse("Done")

def index(request):
    template = loader.get_template('index.html')
    players = usersmanger.get_all_players()
    return HttpResponse(template.render({'players': enumerate(players, 1)}, request))
