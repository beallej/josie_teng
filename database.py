from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from webapp import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Mission(db.Model):
    __tablename__ = 'mission'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    categories = db.Column(db.Text)
    date_saisie = db.Column(db.DateTime)
    date_closed = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.Text)
    ingenieurs_positionnes = relationship("Positionnement", back_populates="mission")
    ingenieur_affectue = relationship("Affectuation", back_populates="mission")

class Ingenieur_Etudes(db.Model):
    __tablename__ = 'ingenieur_etudes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    missions_positiones = relationship("Positionnement", back_populates="ingenieur_etudes")
    missions_affectues = relationship("Affectuation", back_populates="ingenieur_etudes")

class Positionnement(db.Model):
    __tablename__ = 'positionnement'
    voeux = db.Column(db.Text)
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'), primary_key=True)
    ingenieur_etudes_id = db.Column(db.Integer, db.ForeignKey('ingenieur_etudes.id'),  primary_key=True)
    date_positione = db.Column(db.DateTime)
    date_saisie = db.Column(db.DateTime)
    ingenieur_etudes = relationship("Ingenieur_Etudes", back_populates="missions_positiones")
    mission = relationship("Mission", back_populates="ingenieurs_positionnes")

class Affectuation(db.Model):
    __tablename__ = 'affectuation'
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'),  primary_key=True)
    ingenieur_etudes_id = db.Column(db.Integer, db.ForeignKey('ingenieur_etudes.id'),  primary_key=True)
    date_affectue = db.Column(db.DateTime)

    ingenieur_etudes = relationship("Ingenieur_Etudes", back_populates="missions_affectues")
    mission = relationship("Mission", back_populates="ingenieur_affectue")
