from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from enum import Enum


from webapp import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Base = declarative_base()

class Status(Enum):
    A_AFFECTER = "a_affecter"
    CLOS = "clos"
    AFFECTE = "affecte"

def affectuer(mission, ingenieur_etudes):
    affectuation = Affectuation(mission_id=mission.id, ingenieur_etudes_id=ingenieur_etudes.id)
    mission.ingenieurs_affectue = affectuation
    mission.status = Status.AFFECTE
    ingenieur_etudes.missions_affectues.append(affectuation)

association_table = db.Table('association',
    db.Column('mission_id', db.Integer, db.ForeignKey('mission.id')),
    db.Column('category', db.Integer, db.ForeignKey('category.id'))
)

class Mission(db.Model):
    __tablename__ = 'mission'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    categories = relationship(
        "Category",
        secondary=association_table,
        back_populates="missions")
    date_saisie = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_closed = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(Status), default=Status.A_AFFECTER)
    ingenieurs_positionnes = relationship("Positionnement")
    ingenieurs_affectue = relationship("Affectuation", uselist=False)

    def close(self):
        self.date_closed = datetime.datetime.utcnow()
        self.status = Status.CLOS

class Category(db.Model):
    __tablename__ = 'category'
    id = id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    missions = relationship(
        "Mission",
        secondary=association_table,
        back_populates="categories")


class Ingenieur_Etudes(db.Model):
    __tablename__ = 'ingenieur_etudes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    missions_positionnes = relationship("Positionnement")
    missions_affectues = relationship("Affectuation")

    def positionner(self, mission, voeux):
        positionnement = Positionnement(voeux=voeux, ingenieur_etudes_id=self.id, mission_id=mission.id)
        self.missions_positionnes.append(positionnement)

class Action(db.Model):
    __tablename__ = 'action'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'))
    ingenieur_etudes_id = db.Column(db.Integer, db.ForeignKey('ingenieur_etudes.id'))


class Positionnement(Action):
    __tablename__ = 'positionnement'
    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)
    voeux = db.Column(db.Text)


class Affectuation(Action):
    __tablename__ = 'affectuation'
    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)

