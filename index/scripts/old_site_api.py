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
*   row 129: challenges doesn't exist in the challenges table
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
SEVENTY_FIVE = 75

MULTYPOINT_CHALLENGES = (
    u"crackme שימושי כלשהו לצוות רוורסינג",
    "Codingbat Python",
    "Codingbat Java",
    u"משחק Bandit בOverTheWire.org",
    "gracker.org",
    u"אתגרי משחק Narnia בoverthewire.org",
    u"משחק הXSS של גוגל",
    u"אתגרי הXSS של escape.alf.nu",
    "yamagata's XSS challenges"
)

SECURITY_CHALLENGES = {
    "hackthissite.org": TWENTY,
    "IceCTF 2016": TWENTY,
    "hackthis.co.uk": FORTY,
    "hellboundhackers.org": THIRTY,
    "ksnctf": FORTY,
    "RedTiger Hackit": SEVENTY_FIVE,
    "tdhack.com challenge: Net 1 - Amateur job": None,
    "OWASP rhcloud CTF, web challenge 1": None,
    "OWASP rhcloud CTF, web challenge 2": None,
    "OWASP rhcloud CTF, web challenge 3": None,
    "tdhack.com challenge: Net 2 - Safe Java": None,
    "tdhack.com challenge: Net 3 - Once again, I forgot": None,
    "tdhack.com challenge: Net 4 - Few points": None,
    "tdhack.com challenge: Net 5 - Password reminder": None,
    # informatics challenges, built similiar to the security challenges.
    u"תרגום מאמר של 80-250 מילים בויקיפדיה": None,
    u"תרגום מאמר של 250 מילים ומעלה בויקיפדיה": None
}

NONEXISTENT_USERS = (
    "shot4shot",
    "cripyice",
    "cuphead"
)

NONEXISTENT_CHALLENGES = (
    "thisislegal.org",
    u"שמירת קובץ של משחק מחשב",
    u"כתיבה במשחק",
    u"""בגרות קיץ תשע"ד 035005, 4 יח"ל השלמה, שאלה 3"""
)
MULTYPOINT_FUNCTIONS = (
    "codewars",
    "Extreme trainer"   # Ask if we need to create a constant for this name
)


class MultypointChall:
    def __init__(self, data, challenge_name, category):
        """gets challenge name and its category.
        :param data: the data to be analyzed.
        :type data: str.
        :param challenge_name: the name of the challenge.
        :type challenge_name: str.
        :param category: the name of the category the challenge is associated with.
        :type category: str.
        """
        self.data = data
        self.challenge_name = challenge_name
        self.category = category

    def parse(self):
        """parses the given data string to name and points."""
        self.name, self.points = self.data.replace(')', '').split(
            " ")[0], self.data.replace(')', '').split(" ")[-1]

    def update_db(self):
        """updates solution on the database."""
        update_solution(self.name, self.challenge_name,
                        self.category, self.points)


def import_users():
    """imports all the users in page"""
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
    """imports all the users in page"""
    challenges_data = Challenges()
    challenges_tables = challenges_data.get_challenges_tables()
    challenges_name = challenges_data.get_challenges_names()

    all_challenges = import_challenges_organize(
        challenges_tables, challenges_name)

    for category in all_challenges:
        update_category(category['table_name'])
        # someone needs to add to the update_challenge function an option to upload
        # a mentor and times to solve
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
                                 int(float(challenge['points']) + 0.5),
                                 challenge['deadline'])


def import_solutions():
    """import all of the solved challenges from the 2nd page"""
    all_solved_challenges = solved_challenges_table_organize()

    for category in all_solved_challenges:
        for challenge in category['challenges']:
            if challenge['challenge_name'] in NONEXISTENT_CHALLENGES:
                    continue
            for solver in challenge['solvers']:
                if not username_validate(solver.replace(" ", "")):
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


def update_multipoint(data: str, challenge_name: str, category: str):
    """scrapes multipoints challenges that aren't one-time-solve.
    :param data: the data of the solver to be analyzed.
    :type data: str.
    :param challenge_name: name of the challenge.
    :type challenge_name: str.
    :param category: the name of the category associated with the challenge.
    :type category: str.
    """
    chall = MultypointChall(data, challenge_name, category)
    chall.parse()

    if not username_validate(chall.name):
        return
    
    if challenge_name in SECURITY_CHALLENGES:
        security_points_convert(chall)

    chall.update_db()


def security_points_convert(chall):
    """scrapes security challenges.
    :param chall: the challenge to analyze.
    :type chall: str.
    """
    try:
        chall.points = int(chall.points) // SECURITY_CHALLENGES[chall.challenge_name]
        chall.points = int(chall.points + 0.5)
    except ValueError:
        chall.points = 1

        
def exec_multypoints_functions(data, challenge_name, category):
    """Executes the multi-point functions.
    :param data: the data of the solver to be analyzed.
    :type data: str.
    :param challenge_name: the name of the challenge to be analyzed.
    :type challenge_name: str.
    :param category: the name of the category the challenges is in.
    :type category: str.
    """
    challenge_name = "update_" + "_".join(challenge_name.lower().split())

    globals()[challenge_name](data, category)


def update_codewars(data, category):
    """updates the codewars challenge.
    :param data: the solvers data.
    :param category: the category the challenge is in.
    """
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
    """updates the extreme trainer trainer challenge.
    :param data: the data of the solvers to be analyzed.
    :type data: str.
    :param category: the category the challenge is in.
    :type category: str.
    """
    data = data.replace(')', "", 2).replace('(', ')').split(')')

    names = data[0].split(", ")
    points = int(data[1][-1])

    for name in names:
        update_solution(name.replace(" ", ""),
                        "Extreme trainer",
                        category,
                        points)


def username_validate(name):
    """checks if username if valid.
    :param name: the name to validate.
    :type name: str.
    """
    if name.lower() in NONEXISTENT_USERS:
        return 0
    return 1


def update_from_old_site():
    """updates the new site from the old site"""
    import_users()
    import_challenges()
    import_solutions()
