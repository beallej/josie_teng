from service import *
from database import Ingenieur_Etudes


def test_db():

    felipe = Ingenieur_Etudes(name="Felipe")
    pablo = Ingenieur_Etudes(name="Pablo")
    josie = Ingenieur_Etudes(name="Josie")
    db.session.add(felipe)
    db.session.add(pablo)
    db.session.add(josie)
    db.session.commit()

    addMission("go to carrefour", "", ["courses"])
    addMission("apply to jobs", "", ["devoirs"])
    addMission("write cv", "", ["devoirs", "francais"])
    addMission("language exchage", "", ["francais", "social"])

    missions = getMissionsAAffecter()
    missions_devoirs = getMissionsAAffecter(categories=["devoirs"])
    missions_francais = getMissionsAAffecter(categories=["francais"])
    missions_devoirs_francais = getMissionsAAffecter(categories=["devoirs", "francais"])
    assert len(missions_devoirs) == 2
    assert len(missions_devoirs_francais) == 3
    supermarket_mission = getMissionsAAffecter(categories=["courses"])[0]
    felipe.positionner(supermarket_mission, "i want to compare all of the products")
    pablo.positionner(supermarket_mission, "i want felipe to hurry up")

    affectuer(supermarket_mission, pablo)

    pablo_activity = getEvolutionPourIngenier(pablo.id)
    supermarket_voeux= getVoeuxPourMission(supermarket_mission.id)
    cloreMission(supermarket_mission.id)
    supprimerMission(supermarket_mission.id)
    m = 3
    return