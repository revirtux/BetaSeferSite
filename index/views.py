from django.http import HttpResponse, Http404
from django.template import loader
from .managers import usersmanger, housesmanager, categoriesmanager, common
from .scripts.old_site_api import update_from_old_site


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
    players = usersmanger.get_all_players('player')
    zombies = usersmanger.get_all_players('zombie')
    pensioners = usersmanger.get_all_players('pensioner')
    commemorations = usersmanger.get_all_players('commemoration')
    houses = housesmanager.get_all_houses()
    categories = categoriesmanager.get_all_categories()
    return HttpResponse(template.render(
        {
            'players': enumerate(players, 1),
            'zombies': enumerate(zombies, 1),
            'pensioners': enumerate(pensioners, 1),
            'commemorations': enumerate(commemorations, 1),
            'houses': houses,
            'categories': categories
        }, request))

def profile(request, usernick):
    template = loader.get_template('profile.html')
    user = usersmanger.get_user_by_nick(usernick)
    level = usersmanger.dox_user(user).rank.level
    houses = user.houses.all()
    return HttpResponse(template.render(
        {
            'user': user,
            'houses': houses,
            'level': level
        }, request))


def house_path(request, house_name):
    template = loader.get_template('house.html')
    players = usersmanger.get_all_players(house=house_name.title())
    house = housesmanager.get_house(house_name.title())
    return HttpResponse(template.render(
        {
            'players': enumerate(players, 1),
            'house': house
        }, request))


def import_old_site(request):
    update_from_old_site()
    return HttpResponse("Done")


def dynamic_css(request, house_name):
    template = loader.get_template('colors.css')
    resp = HttpResponse(template.render(
        {
            'house': housesmanager.get_house(house_name.title())
        }, request))

    resp['Content-Type'] = 'text/css'
    return resp


def challenges_path(request, category_name):
    category_list = categoriesmanager.get_all_categories().filter(name=category_name)
    if len(category_list) != 0:
        category = category_list[0]
        template = loader.get_template('challenge.html')
        challenges = categoriesmanager.get_all_challenges(category)
        return HttpResponse(template.render(
            {
                'challenges': enumerate(challenges, 1),
                'amount': len(challenges),
                'category': category
            }, request))
    else:
        return Http404("<p>No such category</p>")