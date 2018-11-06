from dto import *
from database import *
from sqlite3 import IntegrityError

def getMissions(status=None):
    if status == None :
        return list(map(MissionResponse, Mission.query.all()))

    return list(map(MissionResponse, Mission.query.filter_by(status=status)))

def getMissionsAffectes():
    return getMissions(status=Status.AFFECTE)

def getMissionsClosed():
    return getMissions(status=Status.CLOS)

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
        return getMissions(status=Status.A_AFFECTER)
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
    categories = csv_to_list(categories)
    for category in categories:
        category_obj = Category.query.filter_by(name=category).first()
        if category_obj is None:
            category_obj = Category(name=category)
            db.session.add(category_obj)
        category_obj.missions.append(new_mission)

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

def create_account(username, password, name, type):
    if type == IngenieurType.Affaires:
        account = Ingenieur_Affaires(username=username, password=password, name=name)
    else:
        account = Ingenieur_Etudes(username=username, password=password, name=name)

    db.session.add(account)
    try:
        db.session.commit()
        return account
    except IntegrityError:
        return Exception("Nom d'utilisateur pas disponible")


def login(username, password):
    ingenieur = Ingenieur_Etudes.query.filter_by(username=username, password=password).first()
    if ingenieur is None :
        ingenieur = Ingenieur_Affaires.query.filter_by(username=username, password=password).first()
    return LoginResponse(ingenieur)




