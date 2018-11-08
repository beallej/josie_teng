from utils import *
from database import *

class IngenieurType(Enum):
    Affaires = "affaires"
    Etudes = "etudes"


class MissionResponse:
    def __init__(self, mission):
        self.id = mission.id
        self.title = mission.title
        self.description = mission.description
        self.categories = list(map(lambda categorie: categorie.name, mission.categories))
        self.status = mission.status.value
        self.date_saisie = date_to_string(mission.date_saisie)
        self.date_closed = date_to_string(mission.date_closed)
        self.date_closed = None if mission.date_closed is None else mission.date_closed.astimezone().strftime(
            "%Y-%m-%d %H:%M:%S")
        self.ingenieurs_positionnees = list(map(IngenieurResponseChild, mission.ingenieurs_positionnes))
        self.ingenieur_affecte = IngenieurResponseChild(
            mission.ingenieurs_affectue) if mission.ingenieurs_affectue else None


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


class LoginResponse:
    def __init__(self, ingenieur):
        self.id = ingenieur.id
        self.name = ingenieur.name
        if isinstance(ingenieur, Ingenieur_Affaires):
            self.type = IngenieurType.Affaires.value
        else:
            self.type = IngenieurType.Etudes.value




class ActionResponse:

    def __init__(self, action):
        self.mission = Mission.query.filter_by(id=action.mission_id).first()
        self.affectue = False
        self.positionne = False
        self.sort_date = action.date
        self.date_affectue = None
        self.date_positionne = None
        self.voeux = None

class PositionnementResponse(ActionResponse):

    def __init__(self, positionnement):
        super(PositionnementResponse, self).__init__(positionnement)
        self.positionne = True
        self.voeux = positionnement.voeux
        self.date_positionne = date_to_string(positionnement.date)

class AffectuationResponse(ActionResponse):

    def __init__(self, affectuation):
        super(AffectuationResponse, self).__init__(affectuation)
        self.affectue = True
        self.date_affectue = date_to_string(affectuation.date)


def format_action_desc(action):
    ingenieur = Ingenieur_Etudes.query.filter_by(id=action.ingenieur_etudes_id).first()
    mission = Mission.query.filter_by(id=action.mission_id).first()
    date = date_to_string(action.date)

