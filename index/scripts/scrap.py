import requests
from bs4 import BeautifulSoup
from ..models.users import USER_STATES
from ..managers.usersmanger import add_user

SITE = 'https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90'


def scrap_users():
    req = requests.get(SITE)
    if req.status_code != 200:
        return
    
    bs = BeautifulSoup(req.text, 'html.parser')
    tables = bs.find_all('table', 'wikitable')

    _, players, zombies, pensioners, commemorations, *_ = tables

    for tr in players.tbody.find_all('tr')[1:]:
        _, nick, *_, houses = tr.find_all('td')
        nick = nick.a.text
        houses = [a.get('title').split(' ')[-1] for a in houses.find_all('a')]
        add_user(nick, USER_STATES['Player'], houses)

    for tr in zombies.tbody.find_all('tr')[1:]:
        _, nick, _, note, *_, houses = tr.find_all('td')
        nick = nick.a.text
        note = note.text
        houses = [a.get('title').split(' ')[-1] for a in houses.find_all('a')]
        add_user(nick, USER_STATES['Zombie'], houses, note=note)

    for tr in pensioners.tbody.find_all('tr')[1:]:
        nick, *_, houses = tr.find_all('td')
        nick = nick.a.text if nick.a else nick.text
        houses = [a.get('title').split(' ')[-1] for a in houses.find_all('a')]
        add_user(nick, USER_STATES['Pensioner'], houses)

    for tr in commemorations.tbody.find_all('tr')[1:]:
        nick, *_ = tr.find_all('td')
        nick = nick.a.text
        add_user(nick, USER_STATES['Commemoration'])