"""
Import tables from the old sites

----------------------------------------------------------------
Exceptions:
----------------------------------------------------------------
*   row 55: Manually add "it4n" to DB - not found in code ninja
    setted as testing user.


"""
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
            if challenge['challenge_name'].lower() == "codewars":      # here I ignored codewars
                continue

            update_challenge(challenge['challenge_name'],
                             category['table_name'],
                             challenge['description'],
                             int(challenge['points']),
                             challenge['deadline'])

# update_solution(user: str, challenge: str, category: str, multipoint: int = 1):
def import_solutions():
    all_solved_challenges = solved_challenges_table_organize()

    for category in all_solved_challenges:
        for challenge in category['challenges']:
            if "codingbat" in challenge['challenge_name'].lower():
                continue
            for solver in challenge['solvers']:     # added user it4n for it to work
                if solver == "it4n":    # missing from the db
                    continue
                if challenge['challenge_name'] == "codewars":
                    update_codewars(solver, category['subject'])
                    continue
                elif solver == "cugz (cugz_advanced_crackme_2)":    # cugz_crackme - ask regev
                    break
                update_solution(solver.replace(" ", ""), challenge['challenge_name'], category['subject'])

# update_challenge(name: str, category: str, description: str = "", score: int = 1)
def update_codewars(data, category):
    solver_data = data.replace(")", "(").split("(")

    name = solver_data[0]
    challenges = solver_data[1].replace(',', '').split()

    challenges_data = [{"color": challenges[i], "points": int(challenges[i + 2])} 
                        for i in range(0, len(challenges), 3)]

    for codewars_challenge in range(len(challenges_data)):
        color, points = challenges_data[codewars_challenge].values()
        update_challenge("Codewars " + color.title() + " Challenges",
                         category,
                         score=codewars_challenge + 1)
        update_solution(name.replace(" ", ""),
                        "Codewars " + color.title() + " Challenges",
                         category,
                         multipoint=points)


def update_multipoints(data, challenge_name, category):
    name, points = data.replace(')', '').split(" ")[0], data.replace(')', '').split(" ")[-1]

    update_solution(name, challenge_name, category, points)


def cugz_crackme():
    # wierd sctructre of solvers
    pass

def update_from_old_site():
    # ss = SiteScrapper()
    #import_users()
    #import_challenges()
    import_solutions()
    pass
