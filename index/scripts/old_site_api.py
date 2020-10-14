"""
Import tables from the old sites

----------------------------------------------------------------
Exceptions:
----------------------------------------------------------------
*   row 26: users are not exist, it4n added to db.
*   row 29: removed CripyIce from משחק הדינוזאור של hexer challenge
    since it has been problematic
*   row 0: removed 'crackme שימושי כלשהו לצוות רוורסינג' challenge from
    Reversing & Pwning category since it appeard twice (also in C catogory)
"""
from .site_scrapper import users_tables_organize, get_main_tables, solved_challenges_table_organize
from .site_scrapper import import_challenges_organize, Scrapper, Challenges
from ..managers.usersmanger import update_user
from ..managers.solutionsmanager import update_solution
from ..managers.challengesmanager import update_challenge
from ..managers.categoriesmanager import update_category

TWENTY = 20
THIRTY = 30
FORTY = 40

MULTYPOINT_CHALLENGES = (
    u"crackme שימושי כלשהו לצוות רוורסינג",
    "Codingbat Python",
    "Codingbat Java",
    u"משחק Bandit בOverTheWire.org",
    "gracker.org",
    u"אתגרי משחק Narnia בoverthewire.org "
)

SECURITY_CHALLENGES = {
    "hackthissite.org": TWENTY
}

NONEXISTENT_USERS = (
    "shot4shot",
    "CripyIce",
    "It4n"
)

MULTYPOINT_FUNCTIONS = (
    "codewars",
    "Extreme trainer"
)


class MultypointChall:
    def __init__(self, data, challenge_name, category):
        self.data = data
        self.challenge_name = challenge_name
        self.category = category

    def parse(self):
        self.name, self.points = self.data.replace(')', '').split(
            " ")[0], self.data.replace(')', '').split(" ")[-1]

    def update_db(self):
        update_solution(self.name, self.challenge_name,
                        self.category, self.points)


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


def import_challenges():
    challenges_data = Challenges()
    challenges_tables = challenges_data.get_challenges_tables()
    challenges_name = challenges_data.get_challenges_names()

    all_challenges = import_challenges_organize(
        challenges_tables, challenges_name)

    for category in all_challenges:
        update_category(category['table_name'])

        for challenge in category['challenges']:
            if challenge['challenge_name'].lower() == "codewars":      # here I ignored codewars
                continue
            elif 'codingbat' in challenge['challenge_name'].lower():
                update_challenge(challenge['challenge_name'],
                                 category['table_name'],
                                 challenge['description'],
                                 0,
                                 challenge['deadline'])
            else:
                update_challenge(challenge['challenge_name'],
                                 category['table_name'],
                                 challenge['description'],
                                 float(challenge['points']),
                                 challenge['deadline'])


def import_solutions():
    all_solved_challenges = solved_challenges_table_organize()

    for category in all_solved_challenges:
        for challenge in category['challenges']:
            for solver in challenge['solvers']:
                if solver in NONEXISTENT_USERS:
                    continue
                if challenge['challenge_name'] in MULTYPOINT_FUNCTIONS:
                    exec_multypoints_functions(
                        solver, challenge['challenge_name'], category['subject'])
                elif challenge['challenge_name'] in MULTYPOINT_CHALLENGES or challenge['challenge_name'] in SECURITY_CHALLENGES:
                    update_multipoint(
                        solver, challenge['challenge_name'], category['subject'])
                elif challenge['challenge_name'] == "Extreme trainer":
                    update_extreme_trainer(solver, category['subject'])
                else:
                    update_solution(
                        solver.replace(" ", ""), challenge['challenge_name'], category['subject'])


def update_multipoint(data, challenge_name, category):
    chall = MultypointChall(data, challenge_name, category)
    chall.parse()

    if challenge_name in SECURITY_CHALLENGES:
        security_points_convert(chall)

    chall.update_db()


def security_points_convert(chall):
    chall.points = int(chall.points) // SECURITY_CHALLENGES[chall.challenge_name]


def exec_multypoints_functions(data, challenge_name, category):
    challenge_name = "update_" + "_".join(challenge_name.lower().split())

    globals()[challenge_name](data, category)


def update_codewars(data, category):
    solver_data = data.replace(")", "(").split("(")

    name = solver_data[0]
    challenges = solver_data[1].replace(',', '').split()

    challenges_data = [{"color": challenges[i], "points": int(
        challenges[i + 2])} for i in range(0, len(challenges), 3)]

    for codewars_challenge in range(len(challenges_data)):
        color, points = challenges_data[codewars_challenge].values()
        update_challenge("Codewars " + color.title(),
                         category,
                         score=codewars_challenge + 1)
        update_solution(name.replace(" ", ""),
                        "Codewars " + color.title(),
                        category,
                        multipoint=points)


def update_extreme_trainer(data, category):
    data = data.replace(')', "", 2).replace('(', ')').split(')')

    names = data[0].split(", ")
    points = int(data[1][-1])

    for name in names:
        update_solution(name.replace(" ", ""),
                        "Extreme trainer",
                        category,
                        points)


def update_from_old_site():
    import_users()
    import_challenges()
    import_solutions()
