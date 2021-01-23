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
    """contains invformation on each table
    """
    status: str
    users: list = field(default_factory=list)
    ninja: bool = False


class Scrapper:
    """scraps tables and headers from the page. applies Beautiful soup on the site."""
    def __init__(self, url):
        """creates the Beautiful element to scrape.
        :param url: the url of the page to scrape.
        :type url: str.
        """
        self.url = url
        self.r = requests.get(self.url)
        self.soup = BeautifulSoup(self.r.text, 'html.parser')

    def soup_all_tables(self):
        """gets all tables in the page into a list.
        :return: list of all tables in the page.
        :rtype: list.
        """
        tables = self.soup.find_all('table')

        return tables


    def soup_main_tables(self):
        """scrapes all the users tables and non-challenges tables.
        :return: all of the users and tables and non-challenges tables.
        :rtype: list.
        """
        main_tables = self.soup.find_all('table', class_="wikitable sortable")

        return main_tables


    def soup_challenges_tables(self):
        """gets all the challenge tables.
        :return: list of the challenge tables.
        :rtype: list.
        """
        challenges_tables = self.soup.find_all('table', class_="wikitable")

        return challenges_tables
    

    def soup_headers(self):
        """gets all the headers tags from the page.
        :return: list of all the headers.
        :rtype: list.
        """
        headers = self.soup.find_all('h3')

        return headers

class Challenges(Scrapper):
    """helps scrape all the challenges in the page.
    :param Scrapper: a class to inherit from.
    :type Scrapper: class.
    """
    def __init__(self):
        """uses the __init__ that inherited from Scrapper class."""
        super().__init__(MAIN_PAGE_URL)
    

    def get_challenges_tables(self):
        """gets all the challenges tables.
        :return: list of challenges.
        :rtype: list.
        """
        challenges_tables = self.soup_challenges_tables()

        return challenges_tables


    def get_challenges_names(self):
        """gets all the titles of the challenges categories
        :return: list of challenges categories titles.
        :rtype: list.
        """
        challenges_names = import_challenges_table_name(self.soup)

        return challenges_names


def download_image(content, title):
    """downloads a given image.
    :param content: bytes to create an image with.
    :type content: byte.
    :param title: Title of the image.
    :type title: str
    """
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
    :return: list of all the users in each category.
    :rtype: list[dataclass(str, list, bool)].
    """

    # Check if the ninja parameter is neccessary
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
    """gets all the active ninjas into users_categories.
    :param users_categories: a list with all the users categories, gets ninjas here.
    :type users_categories: list[dataclass(str, list, bool)].
    :param table: the table of ninjas to be analyzed.
    :type table: bs4 element.
    :param table_index: the index of the ninja table.
    :type table_index: int
    """
    for tr in table.tbody.find_all('tr')[1:]:
        _, name, *_, houses = tr.find_all('td')
        houses = [house['title'].lstrip("House of").lstrip("The") for house in houses.find_all('a')]
        users_categories[table_index].users.append(
            dict({'name': name.a.text, 'houses': houses}))


def zombie_info(users_categories, table):
    """gets all the zombies into users_categories.
    :param users_categories: a list with all the users categories, gets zombies here.
    :type users_categories: list[dataclass(str, list, bool)].
    :param table: the table of zombies to be analyzed.
    :type table: bs4 element.
    """
    for tr in table.tbody.find_all('tr')[1:]:
        _, name, _, remark, *_, houses = tr.find_all('td')

        houses = [house['title'].lstrip("House of").lstrip("The") for house in houses.find_all('a')]
        users_categories[ZOMBIES_TABLE_INDEX].users.append(
            dict({'name': name.a.text, 'houses': houses, 'remarks': remark.text.replace('\n', '')}))


def pension_commemoration_info(users_categories, table, table_index):
    """gets all the beta users in commemoration into users_categories.
    :param users_categories: a list with all the users categories, gets commemoration here.
    :type users_categories: list[dataclass(str, list, bool)].
    :param table: the table of commemoration to be analyzed.
    :type table: bs4 element.
    :param table_index: the index of the commemoration table.
    """
    for tr in table.tbody.find_all('tr')[1:]:
        name, *_, houses = tr.find_all('td')

        if houses.a is not None:
            houses = [house['title'].lstrip("House of").lstrip("The") for house in houses.find_all('a')]

            users_categories[table_index].users.append(
                dict({'name': name.text.replace('\n', ''), 'houses': houses}))
        else:
            users_categories[table_index].users.append(
                dict({'name': name.text.replace('\n', ''), 'houses': []}))


def games_tables_organize(tables) -> list:
    """connect to all of the functions that collects data about the games and organize the data.
    :param tables: all of the tables in the page.
    :type tables: bs4 element
    :return: list
    
    
     of dictionaries with all the games titles and ranks.
    :rtype: list[dict{str, list(str)}].
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
    :rtype: list[dict{str, byte}]
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


def import_challenges_organize(tables, challenges: list) -> list:
    """Connect to all of the functions that collects data about the challenges and organize the data.
    :param tables: all of the tables in the page.
    :type tables: bs4 element.
    :param challenges: list of all the challenges.
    :type list: list
    :return: list of all the challenges.
    :rtype: list
    """
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
    challenges_table_names = [{'table_name': challenges_table_names[i].replace(" Challenges", ""), 'challenges': [
    ]} for i in range(len(challenges_table_names))]

    return challenges_table_names


def import_challenges(table) -> list:
    """Gets the challenges of each category from the page (c, python, java... etc)
    :param table: each table is a new category.
    :type table: bs4 element
    :return: list of the challenges of each category
    :rtype: list[dict{str: int, str: str}]
    """
    challenges = list()

    for row in table.tbody.find_all('tr')[1:]:
        challenge_name, points, mentor, description, solve_times, dl = row.find_all('td')

        dl = dl.text.replace('\n', '')

        if not dl:
            dl = '-'

        challenges.append(dict({'challenge_name': challenge_name.text.replace('\n', ''),
                                'points': points.text.replace('\n', ''),
                                'mentor': mentor,
                                'solve times': solve_times,
                                'description': description.text.replace('\n', ''),
                                'deadline': dl}))

    return challenges


def solved_challenges_table_organize() -> list:
    """connects all of the functions that collects data on solved challenges table & organize it.
    :return: list of solved challenges.
    :rtype: list[dict{str, list[dict{str, list[str]}]}]
    """
    solved_challenges = list()
    second_page_url = 'https://beta.wikiversity.org/wiki/User:The_duke/solved_beta_challenges'

    site_scrapper = Scrapper(second_page_url)
    tables = site_scrapper.soup_all_tables()
    heads = site_scrapper.soup_headers()

    table_names = [table_name.text.replace(
        '[edit]', '').replace(u'אתגרי ', "") for table_name in heads if '[edit]' in table_name.text][:-NON_TECH_TABLES]

    for table_name in range(len(table_names)):
        challenges_and_solvers = import_solved_challenges(tables[table_name])

        table_names[table_name] = " ".join(table_names[table_name].split())
        solved_challenges.append({'subject': table_names[table_name], 'challenges': challenges_and_solvers})

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


def get_pwn_game(table) -> list:
    """gets the ranks nickname & image).
    :param table: the pwn table to be analyzed.
    :type table: bs4 element
    :return: a list of dicts with the rank and image in each.
    :rtype: list[dict{str, byte}]
    """
    ninja_games_ranks = list()

    for row in table.find_all('tr')[1:]:
        try:
            _, image, *_ = row.find_all('td')

            title = image.a['title']
            image_url = 'https:' + image.img['src']

            r = requests.get(image_url)

            download_image(r.content, title)

            ninja_games_ranks.append(
                dict({'title': title, 'image': r.content}))
        except TypeError:
            continue

    return ninja_games_ranks


def limbo_projects(main_projects_in_limbo_table) -> list:
    """gets limbo project table to be analyzed.
    :param main_projects_in_limbo_table: the table to be analyzed.
    :type main_projects_in_limbo_table: bs4 element.
    :rtype: list[dict{str, str, str, str}]
    """
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


def get_main_tables():
    """gets all the tables that needs to be analyzed.
    :return: list of all tables.
    :rtype: list.
    """
    site_scrapper = Scrapper(MAIN_PAGE_URL)
    main_tables = site_scrapper.soup_main_tables()

    return main_tables
