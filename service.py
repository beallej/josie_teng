# add mission in database
from database import *



class MissionResponse:
    def __init__(self, mission):
        id = mission.id
        title = mission.title
        description = mission.description
        categories = list(map(lambda category: category.name, mission.categories))
        status = mission.status
        date_saisie = dateToString(mission.date_saisie)
        date_closed = dateToString(mission.date_closed)
        date_closed = None if mission.date_closed is None else mission.date_closed.astimezone().strftime("%Y-%m-%d %H:%M:%S")

def dateToString(date):
    return None if date is None else date.astimezone().strftime(
        "%Y-%m-%d %H:%M:%S")

class ActionResponse:
    def __init__(self, action):
        date = dateToString(action.date)
        description = format_action_desc(action)

def format_action_desc(action):
    ingenieur = Ingenieur_Etudes.query.filter_by(id=action.ingenieur_etudes_id).first()
    mission = Mission.query.filter_by(id=action.mission_id).first()
    date = dateToString(action.date)

    def format_positionnement_desc(positionnemnt):
        return "{ingenieur} a positionner pour mission {mission_titre} avec les souhaits {voeux} à {date}.".format(ingenieur=ingenieur.name, mission_titre=mission.title, voeux=positionnemnt.voeux,
                                                                                date=date)

    def format_affectuation_desc():
        return "{ingenieur} a été affectué la mission {mission_titre} à {date}.".format(ingenieur=ingenieur.name, mission_titre=mission.title, date=date)

    if (action is Positionnement):
        return format_positionnement_desc(action)
    else:
        return format_affectuation_desc()

def getMissionsAvecStatus(status):
    missions = Mission.query.filter_by(status=status)
    return list(missions)
    # return list(map(MissionResponse, missions))

def getMissionsAffectes():
    return getMissionsAvecStatus(Status.AFFECTE)

def getMissionsClosed():
    return getMissionsAvecStatus(Status.CLOS)

def getVoeuxPourMission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    voeux = list(map(lambda ing: ing.voeux, mission.ingenieurs_positionnes))
    return voeux

def getEvolutionPourIngenier(ingenieur_etudes_id):
    actions = list(Action.query.filter_by(ingenieur_etudes_id=ingenieur_etudes_id))
    actions.sort(key=lambda action1: action1.date)
    return list(map(ActionResponse, actions))

def getMissionsAAffecter(categories=None):
    if categories is None:
        return getMissionsAvecStatus(Status.A_AFFECTER)
    missions_pour_categories = set()
    for category_desire in categories:
        print(category_desire)
        missions_pour_category = Category.query.filter_by(name=category_desire).first().missions
        missions_pour_categories = missions_pour_categories.union(set(missions_pour_category))
        print(Category.query.filter_by(name=category_desire))
    missions_a_affecter_pour_categories = list(filter(lambda mission: mission.status == Status.A_AFFECTER, missions_pour_categories))
    return missions_a_affecter_pour_categories



### ACTIONS


def addMission(title, description, categories):
    new_mission = Mission()
    new_mission.title = title
    new_mission.description = description
    for category in categories:
        category_obj = Category.query.filter_by(name=category).first() or Category(name=category)
        new_mission.categories.append(category_obj)

    # map(lambda category: new_mission.categories.append(Category(name=category)), categories)
    db.session.add(new_mission)
    db.session.commit()

def cloreMission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    mission.close()
    db.session.commit()

def supprimerMission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    db.session.delete(mission)
    db.session.commit()

def positionner_pour_mission(mission_id, ingenieur_etudes_id, voeux):
    mission = Mission.query.filter_by(id=mission_id).first()
    ingenieur_etudes = Mission.query.filter_by(id=ingenieur_etudes_id).first()
    ingenieur_etudes.positionner(mission=mission, voeux=voeux)
    db.session.commit()


def affectuer_mission(mission_id, ingenieur_etudes_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    ingenieur_etudes = Mission.query.filter_by(id=ingenieur_etudes_id).first()
    affectuer(mission=mission, ingenieur_etudes=ingenieur_etudes)
    db.session.commit()

