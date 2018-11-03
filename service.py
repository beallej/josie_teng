# add mission in database
from database import *


class MissionResponse:
    def __init__(self, mission):
        self.id = mission.id
        self.title = mission.title
        self.description = mission.description
        self.categories = list(map(lambda category: category.name, mission.categories))
        self.status = mission.status.value
        self.date_saisie = dateToString(mission.date_saisie)
        self.date_closed = dateToString(mission.date_closed)
        self.date_closed = None if mission.date_closed is None else mission.date_closed.astimezone().strftime("%Y-%m-%d %H:%M:%S")
        self.ingenieurs_positionnees = list(map(IngenieurResponseChild, mission.ingenieurs_positionnes))
        self.ingenieur_affecte = IngenieurResponseChild(mission.ingenieurs_affectue) if mission.ingenieurs_affectue else None

class MissionResponseChild:
    def __init__(self, mission):
        self.id = mission.id
        self.title = mission.title

class IngenieurResponseChild:
    def __init__(self, action):
        self.id = action.ingenieur_etudes_id

class IngenieurResponse:
    def __init__(self, ingenieur_etudes):
        self.id = ingenieur_etudes.id
        self.name = ingenieur_etudes.name
        self.missions_positionnes = list(map(MissionResponseChild, ingenieur_etudes.missions_positionnes))
        self.missions_affectues = list(map(MissionResponseChild, ingenieur_etudes.missions_affectues))



def dateToString(date):
    return None if date is None else date.astimezone().strftime(
        "%Y-%m-%d %H:%M:%S")

class ActionResponse:
    def __init__(self, action):
        self.date = dateToString(action.date)
        self.description = format_action_desc(action)

def format_action_desc(action):
    ingenieur = Ingenieur_Etudes.query.filter_by(id=action.ingenieur_etudes_id).first()
    mission = Mission.query.filter_by(id=action.mission_id).first()
    date = dateToString(action.date)

    def format_positionnement_desc(positionnemnt):
        return "{ingenieur} a positionné pour mission {mission_titre} avec les souhaits {voeux} à {date}.".format(ingenieur=ingenieur.name, mission_titre=mission.title, voeux=positionnemnt.voeux,
                                                                                date=date)

    def format_affectuation_desc():
        return "{ingenieur} a été affectué la mission {mission_titre} à {date}.".format(ingenieur=ingenieur.name, mission_titre=mission.title, date=date)

    if isinstance(action, Positionnement):
        return format_positionnement_desc(action)
    else:
        return format_affectuation_desc()

def getMissionsAvecStatus(status):
    missions = Mission.query.filter_by(status=status)
    return list(map(MissionResponse, missions))

def getMissionsAffectes():
    return getMissionsAvecStatus(Status.AFFECTE)

def getMissionsClosed():
    return getMissionsAvecStatus(Status.CLOS)

def getVoeuxPourMission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    voeux = list(map(lambda ing: ing.voeux, mission.ingenieurs_positionnes))
    return voeux

def getEvolutionPourIngenieur(ingenieur_etudes_id):
    actions = list(Positionnement.query.filter_by(ingenieur_etudes_id=ingenieur_etudes_id))
    actions.extend(Affectuation.query.filter_by(ingenieur_etudes_id=ingenieur_etudes_id))
    actions.sort(key=lambda action1: action1.date)
    return list(map(ActionResponse, actions))

def getMissionsAAffecter(categories=None):
    if categories is None:
        return getMissionsAvecStatus(Status.A_AFFECTER)
    missions_pour_categories = set()
    for category_desire in categories:
        missions_pour_category = Category.query.filter_by(name=category_desire).first().missions
        missions_pour_categories = missions_pour_categories.union(set(missions_pour_category))
    missions_a_affecter_pour_categories = list(map(MissionResponse, filter(lambda mission: mission.status == Status.A_AFFECTER, missions_pour_categories)))
    return missions_a_affecter_pour_categories

def get_mission_by_id(id):
    mission = MissionResponse(Mission.query.filter_by(id=id).first())
    return mission

def get_ingenieur_by_id(id):
    return Ingenieur_Etudes.query.filter_by(id=id).first()

### ACTIONS


def addMission(title, description, categories):
    new_mission = Mission()
    new_mission.title = title
    new_mission.description = description
    for category in categories:
        category_obj = Category.query.filter_by(name=category).first() or Category(name=category)
        new_mission.categories.append(category_obj)

    db.session.add(new_mission)
    db.session.commit()
    return new_mission

def cloreMission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    mission.close()
    db.session.commit()

def supprimerMission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    positionnements = Positionnement.query.filter_by(mission_id=mission_id)
    for positionnement in positionnements:
        ingenieur = positionnement.ingenieur
        ingenieur.missions_positionnes.remove(positionnement)
        db.session.merge(ingenieur)
    affectuation = Affectuation.query.filter_by(mission_id=mission_id).first()
    ingenieur = affectuation.ingenieur
    ingenieur.missions_affectues.remove(affectuation)
    db.session.merge(ingenieur)
    for category in mission.categories:
        category.missions.remove(mission)
        db.session.merge(category)
    map(db.session.delete, list(positionnements))
    db.session.delete(affectuation)
    db.session.delete(mission)
    db.session.commit()

def positionner_pour_mission(mission_id, ingenieur_etudes_id, voeux):
    ingenieur_etudes = Ingenieur_Etudes.query.filter_by(id=ingenieur_etudes_id).first()
    ingenieur_etudes.positionner(mission_id=mission_id, voeux=voeux)
    db.session.commit()


def affectuer_mission(mission_id, ingenieur_etudes_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    mission.affectuer(ingenieur_etudes_id)
    db.session.commit()



### Accounts
def create_account_pour_ingenieur_etudes(username, password, name):
    account = Ingenieur_Etudes(username=username, password=password, name=name)
    db.session.add(account)
    db.session.commit()
    return account


def create_account_pour_ingenieur_affaires(username, password, name):
    account = Ingenieur_Affaires(username=username, password=password, name=name)
    db.session.add(account)
    db.session.commit()
    return account


def login(username, password):
    ingenieur = Ingenieur_Etudes.query.filter_by(username=username, password=password).first()
    if ingenieur is None :
        ingenieur = Ingenieur_Affaires.query.filter_by(username=username, password=password).first()
    return ingenieur

