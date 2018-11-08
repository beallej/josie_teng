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
        self.ingenieurs_positionnees = list(map(PositionnementResponse, mission.ingenieurs_positionnes))
        self.ingenieur_affecte = None
        if mission.ingenieurs_affectue:
            self.ingenieur_affecte = AffectuationResponse(mission.ingenieurs_affectue)
            self.ingenieur_affecte.update_with_voeux_from_correstponding_positionnement(self.ingenieurs_positionnees)


class LoginResponse:
    def __init__(self, ingenieur):
        self.id = ingenieur.id
        self.name = ingenieur.name
        if isinstance(ingenieur, Ingenieur_Affaires):
            self.type = IngenieurType.Affaires.value
        else:
            self.type = IngenieurType.Etudes.value




class ActionResponse:

    def __init__(self, action, mission=None):
        self.mission = mission or Mission.query.filter_by(id=action.mission_id).first()
        self.affectue = False
        self.positionne = False
        self.sort_date = action.date
        self.date_affectue = None
        self.date_positionne = None
        self.voeux = None
        self.ingenieur_etudes_id = action.ingenieur_etudes_id
        self.ingenieur_etudes_name = Ingenieur_Etudes.query.filter_by(id=self.ingenieur_etudes_id)

class PositionnementResponse(ActionResponse):

    def __init__(self, positionnement, mission=None):
        super(PositionnementResponse, self).__init__(positionnement, mission)
        self.positionne = True
        self.voeux = positionnement.voeux
        self.date_positionne = date_to_string(positionnement.date)

class AffectuationResponse(ActionResponse):

    def __init__(self, affectuation, mission=None):
        super(AffectuationResponse, self).__init__(affectuation, mission)
        self.affectue = True
        self.date_affectue = date_to_string(affectuation.date)

    def update_with_voeux_from_correstponding_positionnement(self, positionnements):
        positionnements = list(filter(lambda positionnement : positionnement.ingenieur_etudes_id == self.ingenieur_etudes_id, positionnements))
        if len(positionnements) > 0:
            self.voeux = positionnements[0].voeux

