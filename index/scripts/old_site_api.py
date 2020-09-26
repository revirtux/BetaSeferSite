import json
import requests
from bs4 import BeautifulSoup
from .site_scrapper import users_tables_organize, get_main_tables, solved_challenges_table_organize
from .site_scrapper import import_challenges_organize, get_challenges_tables, get_challenges_names
from ..managers.usersmanger import update_user
from ..managers.solutionsmanager import update_solution
from ..managers.challengesmanager import update_challenge, update_category


# update_user(nick: str, state: str, houses: list = [], note: str = "")
def import_users():
    main_tables = get_main_tables()
    users_categories = users_tables_organize(main_tables)

    for users_table in users_categories:
        for user in users_table.users:
            if "remarks" not in user:
                update_user(user['name'], users_table.status, user['houses'])
            else:
                update_user(user['name'], users_table.status,
                            user['houses'], user['remarks'])



# update_challenge(name: str, category: str, description: str = "", score: int = 1)
# update_category(name: str, description: str = "", manager: str = "")
def import_challenges():
    challenges_tables = get_challenges_tables()
    challenges_name = get_challenges_names()

    all_challenges = import_challenges_organize(challenges_tables, challenges_name)

    for category in all_challenges:
        update_category(category['table_name'])

        for challenge in category['challenges']:
            if '/' in challenge['points']:
                challenge['points'] = 1

            update_challenge(challenge['challenge_name'],
                             category['table_name'],
                             challenge['description'],
                             int(challenge['points']),
                             challenge['deadline'])

# update_solution(user: str, challenge: str, multipoint: int = 1):
def import_solutions():
    all_solved_challenges = solved_challenges_table_organize()

    for category in all_solved_challenges:
        update_category(category['subject'])

        for challenge in category['challenges']:
            for solver in challenge['solvers']:
                update_solution(solver, challenge['challenge_name'], category['subject'])


def update_from_old_site():
    # ss = SiteScrapper()
    import_users()
    import_challenges()
    import_solutions()
    pass
