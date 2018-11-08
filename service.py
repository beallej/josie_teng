from dto import *
from database import *

def get_missions(status=None):
    if status == None :
        return list(map(MissionResponse, Mission.query.all()))

    return list(map(MissionResponse, Mission.query.filter_by(status=status)))

def get_missions_affectes():
    return get_missions(status=Status.AFFECTE)

def get_missions_closes():
    return get_missions(status=Status.CLOS)

def get_voeux_pour_mission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    voeux = list(map(lambda ing: ing.voeux, mission.ingenieurs_positionnes))
    return voeux

def get_evolution_pour_ingenieur(ingenieur_etudes_id):
    actions = list(Positionnement.query.filter_by(ingenieur_etudes_id=ingenieur_etudes_id))
    actions.extend(Affectuation.query.filter_by(ingenieur_etudes_id=ingenieur_etudes_id))
    actions.sort(key=lambda action1: action1.date)
    return list(map(ActionResponse, actions))

def get_missions_a_affecter(categories=None):
    if categories is None:
        return get_missions(status=Status.A_AFFECTER)
    missions_pour_categories = set()
    for categorie_desire in categories:
        missions_pour_categorie = Categorie.query.filter_by(name=categorie_desire).first().missions
        missions_pour_categories = missions_pour_categories.union(set(missions_pour_categorie))
    missions_a_affecter_pour_categories = list(map(MissionResponse, filter(lambda mission: mission.status == Status.A_AFFECTER, missions_pour_categories)))
    return missions_a_affecter_pour_categories

def get_mission_by_id(id):
    mission = MissionResponse(Mission.query.filter_by(id=id).first())
    return mission

def get_ingenieur_by_id(id):
    return Ingenieur_Etudes.query.filter_by(id=id).first()




### ACTIONS

def add_mission(title, description, categories):
    new_mission = Mission()
    new_mission.title = title
    new_mission.description = description
    categories = csv_to_list(categories)
    for categorie in categories:
        categorie_obj = Categorie.query.filter_by(name=categorie).first()
        if categorie_obj is None:
            categorie_obj = Categorie(name=categorie)
            db.session.add(categorie_obj)
        categorie_obj.missions.append(new_mission)

    db.session.add(new_mission)
    db.session.commit()
    return new_mission

def clore_mission(mission_id):
    mission = Mission.query.filter_by(id=mission_id).first()
    mission.cloire()
    db.session.commit()

def supprimer_mission(mission_id):
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
    for categorie in mission.categories:
        categorie.missions.remove(mission)
        db.session.merge(categorie)
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
    encrypted_password = encrypt_password(password)
    if type == IngenieurType.Affaires:
        account = Ingenieur_Affaires(username=username, password=encrypted_password, name=name)
    else:
        account = Ingenieur_Etudes(username=username, password=encrypted_password, name=name)
    db.session.add(account)
    try:
        db.session.commit()
        return account
    except Exception:
        db.session.rollback()
        raise Exception("Nom d'utilisateur pas disponible")


def login(username, password):
    encrypted_password = encrypt_password(password)
    ingenieur = Ingenieur_Etudes.query.filter_by(username=username, password=encrypted_password).first()
    print("username " + username)
    if ingenieur is None:
        ingenieur = Ingenieur_Affaires.query.filter_by(username=username, password=encrypted_password).first()
    if ingenieur is None:
        return None
    return LoginResponse(ingenieur)




