from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime
from enum import Enum

from init import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Base = declarative_base()

class Status(Enum):
    A_AFFECTER = "À Affecter"
    CLOS = "Clos"
    AFFECTE = "Affectée"



association_table = db.Table('association',
    db.Column('mission_id', db.Integer, db.ForeignKey('mission.id')),
    db.Column('categorie', db.Integer, db.ForeignKey('categorie.id'))
)


class Mission(db.Model):
    __tablename__ = 'mission'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    categories = relationship(
        "Categorie",
        secondary=association_table,
        back_populates="missions")
    date_saisie = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_closed = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Enum(Status), default=Status.A_AFFECTER)
    ingenieurs_positionnes = relationship("Positionnement", back_populates="mission")
    ingenieurs_affectue = relationship("Affectuation", uselist=False, back_populates="mission")


    def affectuer(self, ingenieur_id):
        affectuation = Affectuation(mission_id=self.id, ingenieur_etudes_id=ingenieur_id)
        self.ingenieurs_affectue = affectuation
        self.status = Status.AFFECTE
        self.ingenieurs_affectue = affectuation


    def clore(self):
        self.date_closed = datetime.datetime.utcnow()
        self.status = Status.CLOS

class Categorie(db.Model):
    __tablename__ = 'categorie'
    id = id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, unique=True)
    missions = relationship(
        "Mission",
        secondary=association_table,
        back_populates="categories")


class Ingenieur(db.Model):
    __tablename__ = 'ingenieur'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)


class Ingenieur_Affaires(Ingenieur):
    __tablename__ = 'ingenieur_affaires'
    id = db.Column(db.Integer, db.ForeignKey('ingenieur.id'), primary_key=True)

class Ingenieur_Etudes(Ingenieur):
    __tablename__ = 'ingenieur_etudes'
    id = db.Column(db.Integer, db.ForeignKey('ingenieur.id'), primary_key=True)

    missions_positionnes = relationship("Positionnement", back_populates="ingenieur")
    missions_affectues = relationship("Affectuation", back_populates="ingenieur")

    def positionner(self, mission_id, voeux):
        positionnement = Positionnement(voeux=voeux, ingenieur_etudes_id=self.id, mission_id=mission_id)
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
    mission = relationship("Mission", back_populates="ingenieurs_positionnes")
    ingenieur = relationship("Ingenieur_Etudes", back_populates="missions_positionnes")



class Affectuation(Action):
    __tablename__ = 'affectuation'
    id = db.Column(db.Integer, db.ForeignKey('action.id'), primary_key=True)
    mission = relationship("Mission", back_populates="ingenieurs_affectue")
    ingenieur = relationship("Ingenieur_Etudes", back_populates="missions_affectues")



