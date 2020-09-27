"""
Import tables from the old sites

----------------------------------------------------------------
Exceptions:
----------------------------------------------------------------
*   row 26: ingnored last 4 tables.
*   row 29: ignored resources table.


"""

import json
import codecs
import requests
from os import mkdir
from bs4 import BeautifulSoup
from dataclasses import dataclass, field

LIMBO_PROJECTS_TABLE_INDEX = -1
PWN_GAME_TABLE_INDEX = -4
NINJAS_TABLE_INDEX = 0
ACTIVES_TABLE_INDEX = 1
ZOMBIES_TABLE_INDEX = 2
PENSIONS_TABLE_INDEX = 3
COMMEMORATION_TABLE_INDEX = 4
NON_TECH_TABLES = 4
TABLE_OFFSET = 15
LAST_CHALLENGES_TABLE = 36  # actually 37, ignored resources table
USELESS_TABLE_1 = 17
USELESS_TABLE_2 = 19
MAIN_PAGE_URL = "https://beta.wikiversity.org/wiki/%D7%9C%D7%99%D7%9E%D7%95%D7%93%" \
    "D7%99_%D7%9E%D7%97%D7%A9%D7%91%D7%99%D7%9D_%D7%91%D7%A9%D7%99%D7%98%D7%AA_%D7%91%D7%98%D7%90"


@dataclass
class UsersTable:
    status: str
    users: list = field(default_factory=list)
    ninja: bool = False


def soup_site(url):
    r = requests.get(url)

    return BeautifulSoup(r.text, 'html.parser')


def write_content(path: str, content):
    """Writes the content of the found users and solved challenges to a file.
    :param path: where the file will be save.
    :type path: str
    :param content: the cotent to be written into the file.
    """
    while True:
        try:
            with codecs.open(path, 'w', encoding='utf-8') as file:
                json.dump(content, file, ensure_ascii=False)

                break
        except IOError:
            mkdir(path[:path.index('\\')])


def download_image(content, title):
    while True:
        try:
            with open("pics\\" + title + ".png", "wb") as file:
                file.write(content)

                break
        except FileNotFoundError:
            mkdir("pics")


def users_tables_organize(tables):
    """connect to all the function that collects data about users and organize the data.
    :param tables: all of the tables in the page.
    :type tables: bs4 element.
    """
    users_categories = [UsersTable('player', ninja=True),
                        UsersTable('player'),
                        UsersTable('zombie'),
                        UsersTable('pensioner'),
                        UsersTable('commemoration')]

    ninja, active, zombie, pension, commemoration, *_ = tables

    ninja_active(users_categories, ninja, NINJAS_TABLE_INDEX)
    ninja_active(users_categories, active, ACTIVES_TABLE_INDEX)
    zombie_info(users_categories, zombie)
    pension_commemoration_info(users_categories, pension, PENSIONS_TABLE_INDEX)
    pension_commemoration_info(users_categories, commemoration, COMMEMORATION_TABLE_INDEX)

    return users_categories


def ninja_active(users_categories, table, table_index):
    for tr in table.tbody.find_all('tr')[1:]:
        _, name, *_, houses = tr.find_all('td')
        houses = [house['title'].lstrip("House of").lstrip("The") for house in houses.find_all('a')]
        users_categories[table_index].users.append(
            dict({'name': name.a.text, 'houses': houses}))


def zombie_info(users_categories, table):
    for tr in table.tbody.find_all('tr')[1:]:
        _, name, _, remark, *_, houses = tr.find_all('td')

        houses = [house['title'].lstrip("House of").lstrip("The") for house in houses.find_all('a')]
        users_categories[ZOMBIES_TABLE_INDEX].users.append(
            dict({'name': name.a.text, 'houses': houses, 'remarks': remark.text.replace('\n', '')}))


def pension_commemoration_info(users_categories, table, table_index):
    for tr in table.tbody.find_all('tr')[1:]:
        name, *_, houses = tr.find_all('td')

        if houses.a is not None:
            houses = [house['title'].lstrip("House of").lstrip("The") for house in houses.find_all('a')]

            users_categories[table_index].users.append(
                dict({'name': name.text.replace('\n', ''), 'houses': houses}))
        else:
            users_categories[table_index].users.append(
                dict({'name': name.text.replace('\n', ''), 'houses': []}))


def games_tables_organize(tables):
    """connect to all of the functions that collects data about the games and organize the data.
    :param tables: all of the tables in the page.
    :type tables: bs4 element
    """
    games = [{'name': 'samorai_c', 'ranks': []},
             {'name': 'python_slayer', 'ranks': []},
             {'name': 'coffee_makers', 'ranks': []}]

    *_, samorai_c, python_slayer, coffee_makers, _, _, _, _ = tables

    for i, game_name in enumerate([samorai_c, python_slayer, coffee_makers]):
        games[i]['ranks'] = import_games(game_name)

    return games


def import_games(table) -> list:
    """Gets all the games of beta and the first 3 rankes.
    :param table: the context to be analyzed.
    :type table: bs4 element
    :return: game table with the name of it and first 3 ranks.
    :rtype: list
    """
    ranks = list()

    for row in table.find_all('tr')[1:4]:
        *_, title, _, image = row.find_all('td')

        title = title.text.replace('\n', '')
        image = image.a.img['src']

        r = requests.get('https:' + image)

        download_image(r.content, title)

        ranks.append(dict({'title': title, 'image': r.content}))

    return ranks


def import_challenges_organize(tables, challenges: list):
    for table in range(TABLE_OFFSET, LAST_CHALLENGES_TABLE):
        if table != USELESS_TABLE_1 and table != USELESS_TABLE_2:
            challenges[table - TABLE_OFFSET - (table > USELESS_TABLE_1) - (
                table > USELESS_TABLE_2)]['challenges'] = import_challenges(tables[table])

    return challenges


def import_challenges_table_name(soup) -> list:
    """Gets the challenges names from the page (c, python, java... etc)
    :param soup: all of the page in 'lxml' format.
    :type soup: bs4 element
    :return: list of the challenges names
    :rtype: list[dict{str, list[str]}]
    """
    challenges_table_names = list()
    div_tags = soup.find_all('div', class_="mw-content-ltr")

    for div_tag in div_tags:
        li_tags = div_tag.find_all('li', class_="toclevel-1 tocsection-54")

        for li_tag in li_tags:
            challenges_table_names = [challenge_name.text for challenge_name in li_tag.find_all(
                'span', class_="toctext")[1:]]

            break
    challenges_table_names = [{'table_name': challenges_table_names[i], 'challenges': [
    ]} for i in range(len(challenges_table_names))]

    return challenges_table_names


def import_challenges(table) -> list:
    """Gets the challenges of each category from the page (c, python, java... etc)
    :param table: each table is a new category.
    :type table: bs4 element
    :return: list of the challenges of each category
    :rtype: list
    """
    challenges = list()

    for row in table.tbody.find_all('tr')[1:]:
        challenge_name, points, _, description, _, dl = row.find_all('td')

        dl = dl.text.replace('\n', '')

        if dl == '':
            dl = '-'

        challenges.append(dict({'challenge_name': challenge_name.text.replace('\n', ''),
                                'points': points.text.replace('\n', ''),
                                'description': description.text.replace('\n', ''),
                                'deadline': dl}))

    return challenges


def solved_challenges_table_organize():
    """connects to all of the functions that collects data on the solved challenges table an organize
         the data.
    """
    solved_challenges = list()
    second_page_url = 'https://beta.wikiversity.org/wiki/User:The_duke/solved_beta_challenges'

    soup = soup_site(second_page_url)
    tables = soup.find_all('table')
    heads = soup.find_all('h3')

    table_names = [table_name.text.replace(
        '[edit]', '').replace(u'אתגרי ', "challenges ") for table_name in heads if '[edit]' in table_name.text][:-NON_TECH_TABLES]

    for table_name in range(len(table_names) - NON_TECH_TABLES):
        challenges_and_solvers = import_solved_challenges(tables[table_name])

        table_names[table_name] = " ".join(table_names[table_name].split()[::-1])
        solved_challenges.append(
            {'subject': table_names[table_name].title(), 'challenges': challenges_and_solvers})

    return solved_challenges[:-1]


def import_solved_challenges(table) -> list:
    """Gets the solved challenges and their solvers.
    :param table: the context to be analyzed (isnt the same as the previous ones).
    :type table: bs4 element
    :return: challenges name and its solvers.
    :rtype: list[dict{str, list[str]}]
    """
    solved_challenges_table = list()

    for row in table.find_all('tr')[1:]:
        challenge_name, solvers = row.find_all('td')
        challenge_name = challenge_name.text.replace('\n', '')
        solvers = solvers.text.replace('\n', '').split('* ')[1:]
        solved_challenges_table.append(
            dict({'challenge_name': challenge_name, 'solvers': solvers}))

    return solved_challenges_table


def get_pwn_game(table):
    ninja_games_ranks = list()

    for row in table.find_all('tr')[1:]:
        try:
            _, image, *_ = row.find_all('td')

            title = image.a['title']
            image_url = 'https:' + image.img['src']

            r = requests.get(image_url)

            download_image(r.content, title)

            ninja_games_ranks.append(
                dict({'title': title, 'image': str(r.content)}))
        except TypeError:
            continue

    return ninja_games_ranks


def limbo_projects(main_projects_in_limbo_table):
    projects = list()

    for row in main_projects_in_limbo_table.find_all('tr')[1:]:
        project_name, contact, description, last_seen = row.find_all('td')
        project_name = project_name.text.replace('\n', '')
        contact = contact.text.replace('\n', ', ')
        description = description.text.replace('\n', '')
        last_seen = last_seen.text.replace('\n', '')

        projects.append({'project_name': project_name,
                         'contact': contact,
                         'description': description,
                         'last_seen': last_seen})

    return projects


def soup_main_tables(soup):
    main_tables = soup.find_all('table', class_="wikitable sortable")

    return main_tables


def soup_challenges_tables(soup):
    challenges_tables = soup.find_all('table', class_="wikitable")

    return challenges_tables


def get_main_tables():
    site_scrapper = soup_site(MAIN_PAGE_URL)
    main_tables = soup_main_tables(site_scrapper)

    return main_tables


def get_challenges_tables():
    site_scrapper = soup_site(MAIN_PAGE_URL)
    challenges_tables = soup_challenges_tables(site_scrapper)

    return challenges_tables


def get_challenges_names():
    site_scrapper = soup_site(MAIN_PAGE_URL)

    challenges_names = import_challenges_table_name(site_scrapper)

    return challenges_names


def main():
    main_tables = get_main_tables()
    challenges_tables = get_challenges_tables()

    # Dump users to json
    users = users_tables_organize(main_tables)
    write_content("users\\json_users.json", users)

    games = games_tables_organize(main_tables)
    for game in games:
        write_content("games\\" + game['name'] + ".json", game['ranks'])

    solved_challenges = solved_challenges_table_organize()
    for solved_challenge in solved_challenges:
        write_content('solved_challenges\\' +
                      solved_challenge['subject'] + '.json', solved_challenge)

    challenges = import_challenges_organize(challenges_tables, challenges)
    for solved_challenge in solved_challenges:
        write_content('solved_challenges\\' +
                      solved_challenge['subject'] + '.json', solved_challenge)

    pwn_game = get_pwn_game(main_tables[PWN_GAME_TABLE_INDEX])
    write_content("Ninja_games\\pwn_game.json", pwn_game)

    projects = limbo_projects(main_tables[LIMBO_PROJECTS_TABLE_INDEX])
    write_content("projects\\limbo_projects.json", projects)
