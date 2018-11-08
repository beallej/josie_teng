import flask
from flask import Flask, request, render_template, flash, session, url_for, redirect
from service import *

from service import *
from utils import *

app = Flask(__name__)
app.secret_key = 'ytkey'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# Login
@app.route('/', methods=['GET', 'POST'])
def index():
    error_message = None
    if request.method == 'POST':
        # get data from html
        username = request.form["username"]
        password = request.form["password"]
        type = request.form["type"]
        if username == "" or password == "":
            error_message = "Nom d'utilisateur ou mot de passe incorrect"
            return render_template('login.html', error_message=error_message)
        else:
            ingenieur = login(username, password)
            if ingenieur != None:
                print("ingenieur.type = " + ingenieur.type)
                print("type = " + type)
                if ingenieur.type == "etudes" and type == "Etudes":
                    print("Etude login success")
                    url = url_for("ingenieur_etudes", ingenieur_id=ingenieur.id)
                    set_cookies(ingenieur)
                    return redirect(url)

                elif ingenieur.type == "affaires" and type == "Affaires":
                    print("Affaire login success")
                    url = url_for("ingenieur_affaires", ingenieur_id=ingenieur.id)
                    set_cookies(ingenieur)
                    return redirect(url)
                else:
                    error_message = "Connexion impossible"
                    print("choisir la correct position svp")
            else:
                error_message = "Nom d'utilisateur ou mot de passe incorrect"

    return render_template('login.html', error_message=error_message)

def set_cookies(ingenieur):
    ingenieur_dict = {'id': ingenieur.id, 'name': ingenieur.name, 'type': ingenieur.type, 'username': ingenieur.username}
    session["ingenieur"] = ingenieur_dict

@app.route('/ingenieur_etudes/<id>/positionner', methods=['POST'])
def positionner(id):
    mission_id = request.form["mission_id"]
    voeux = request.form["reason"]
    positionner_pour_mission(mission_id, id, voeux)
    return redirect(url_for('ingenieur_etudes', ingenieur_id=id))


@app.route('/mission/<id>', methods=['GET'])
def voir_mission_detail(id):
    mission = get_mission_by_id(id)
    ingenieur_logged_in = get_ingenieur_by_id(session["ingenieur"]["id"])
    return render_template('mission.html', mission=mission, ingenieur=ingenieur_logged_in)

@app.route('/mission/<id>/affectuer', methods=['POST'])
def affectuer_mission(id):
    ingenieur_etudes_id = request.form["ingenieur_etudes_id"]
    ingenieur_affaires_id = request.form["ingenieur_affairs_id"]
    affectuer_mission__from_db(id, ingenieur_etudes_id)
    return redirect(url_for('ingenieur_affaires', ingenieur_id=ingenieur_affaires_id))


@app.route('/ingenieur_affaires/<ingenieur_id>/supprimer', methods=['POST'])
def supprimer_mission(ingenieur_id):
    mission_id = request.form["mission_id"]
    supprimer_mission_from_db(mission_id)
    ingenieur_aff = get_ingenieur_affaires_by_id(ingenieur_id)
    ingenieurs = get_all_ingenieurs_etudes()
    return redirect(url_for('ingenieur_affaires', ingenieur_id=ingenieur_id, ingenieurs=ingenieurs,
                            ingenieur_aff=ingenieur_aff))


@app.route('/ingenieur_affaires/<ingenieur_id>/clore', methods=['POST'])
def clore_mission(ingenieur_id):
    mission_id = request.form["mission_id"]
    clore_mission__from_db(mission_id)
    ingenieur_aff = get_ingenieur_affaires_by_id(ingenieur_id)
    ingenieurs = get_all_ingenieurs_etudes()
    return redirect(url_for('ingenieur_affaires', ingenieur_id=ingenieur_id, ingenieurs=ingenieurs,
                            ingenieur_aff=ingenieur_aff))


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    error_message = None
    if request.method == 'POST':
        # get data from html
        username = request.form["username"]
        password = request.form["password"]
        password2 = request.form["password2"]
        name = request.form["name"]
        type = request.form["type"]
        if username == "" or password == "" or password2 == "" or name == "":
            print("No username or No password or No confirmpassword or name")
        elif password == password2:
            try:
                if type == "Etudes":
                    ingenieur = create_account(username, password, name, IngenieurType.Etudes)
                    set_cookies(ingenieur)
                    return redirect(url_for('ingenieur_etudes', ingenieur_id=ingenieur.id))
                else:  # "Affaire"
                    ingenieur = create_account(username, password, name, IngenieurType.Affaires)
                    set_cookies(ingenieur)
                    return redirect(url_for('ingenieur_affaires', ingenieur_id=ingenieur.id))
            except Exception as inst:
                print(inst.args)
                error_message = inst.args[0]

    return render_template('Register.html', error_message=error_message)


# add Mission
@app.route('/ingenieur_affaires/<ingenieur_id>/addmission', methods=['GET', 'POST'])
def add_mission(ingenieur_id):
    ingenieur = get_ingenieur_affaires_by_id(ingenieur_id)
    if request.method == 'POST':
        # get data from html
        title = request.form["title"]
        description = request.form["description"]
        categories = request.form["categories"]
        if title == "" or description == "" or categories == "":
            print("No title or No description")
        else:
            # add mission in database
            add_mission_to_database(title, description, categories)
            print("add successfully")
    return render_template('addmission.html', ingenieur=ingenieur)


# show Missions

@app.route('/ingenieur_etudes/<ingenieur_id>',methods=['GET', 'POST'])
def ingenieur_etudes(ingenieur_id):
    ingenieur = get_ingenieur_etudes_by_id(ingenieur_id)
    categories_list = None
    if request.method == 'POST':
        categories_raw = request.form["categories"]
        categories_list = csv_to_list(categories_raw.lower())
    missions_a_affecter = get_missions_a_affecter_pas_positionner_par_ingenieur(ingenieur_id, categories_list)

    return render_template('ingenieur_etudes.html', missionsAAffecter=missions_a_affecter,
                           ingenieur=ingenieur)


# show Missions
@app.route('/ingenieur_affaires/<ingenieur_id>', methods=['GET', 'POST'])
def ingenieur_affaires(ingenieur_id):
    missionsAAffecter = get_missions_a_affecter()
    missionsAffectes = get_missions_affectes()
    missionsClosed = get_missions_closes()
    ingenieur_aff = get_ingenieur_affaires_by_id(ingenieur_id)
    ingenieurs = get_all_ingenieurs_etudes()
    return render_template('ingenieur_affaires.html', missionsAAffecter=missionsAAffecter,
                           missionsAffectes=missionsAffectes,
                           missionsClosed=missionsClosed,
                           ingenieur_aff=ingenieur_aff,
                           ingenieurs=ingenieurs)


@app.route('/ingenieur_etudes/<ingenieur_id>/activites')
def show_evolution_for_ingenieur(ingenieur_id):
    activites = get_evolution_pour_ingenieur(ingenieur_id)
    times_positionne = count_positionnements(activites)
    times_affectue = count_affectuations(activites)
    ingenieur = get_ingenieur_etudes_by_id(ingenieur_id)
    ingenieur_logged_in = session["ingenieur"]
    return render_template('ingenieur_evolution.html', activites=activites, times_positionne=times_positionne, times_affectue=times_affectue, ingenieur=ingenieur, ingenieur_logged_in=ingenieur_logged_in)


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html')


if __name__ == "__main__":
    from database import db

    # print("creating database")
    # db.drop_all()
    db.create_all()
    # from test import *
    #
    # # test_db()
    # # print("database created")
    app.jinja_env.auto_reload = True
    app.run()
