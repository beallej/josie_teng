import flask
from flask import Flask, request, render_template, flash, session, url_for, redirect
from service import *

from service import *

app = Flask(__name__)
app.secret_key = 'ytkey'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True


# Login
@app.route('/login', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # get data from html
        username = request.form["username"]
        password = request.form["password"]
        type = request.form["type"]
        if username == "" or password == "":
            wrongMsg = True
            print("No username or No password")
            return render_template('login.html', wrongMsg=wrongMsg)
        else:
            ingenieur = login(username,password)
            if ingenieur != None :
                print("ingenieur.type = " + ingenieur.type)
                print("type = " + type)
                if ingenieur.type == "etudes" and type == "Etudes" :
                    print("Etude login success")
                    missions = get_missions()
                    url = url_for("showMissions", ingenieur_id=ingenieur.id)
                    print(url)
                    # redirect(url)
                    # return render_template('showmissions.html',ingenieur=ingenieur,missions=missions)
                    # flask.redirect(flask.url_for("show_missions"),ingenieur_id=ingenieur.id)
                    return redirect(url)

                elif ingenieur.type == "affaires" and type == "Affaires":
                    print("Affaire login success")
                    missions = get_missions()
                    # return render_template('showmissions.html', ingenieur=ingenieur, missions=missions)
                    url_for("show_missions", ingenieur_id=ingenieur.id)
                else:
                    print("choisir la correct position svp")
            else:
                print("login defeat")
                # return render_template('login.html')
    return render_template('login.html')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
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
            # if existe? same username
            try:
                if type == "Etudes" :
                    create_account(username, password, name, IngenieurType.Etudes)
                    print("create account etude successful")
                else: # "Affaire"
                    create_account(username, password, name, IngenieurType.Affaires)
                    print("create account affaire successful")
            except Exception as inst:
                print(inst.args)
                ##TODO DISPLAY EXCEPTION


    return render_template('Register.html')


# add Mission
@app.route('/showmissions/<ingenieur_id>/addmission', methods=['GET', 'POST'])
def addMission(ingenieur_id):
    if request.method == 'POST':
        # get data from html
        title = request.form["title"]
        description = request.form["description"]
        categories = request.form["categories"]
        print(title)
        print(categories)
        if title == "" or description == "":
            print("No title or No description")
        # add mission in database
        add_mission(title, description, categories)

        print("add successfully")
    return render_template('addmission.html',ingenieur_id=ingenieur_id)

# show Missions
@app.route('/showmissions/<ingenieur_id>',methods=['GET','POST'])
def showMissions(ingenieur_id):
    # missions = get_missions()
    missionsAAffecter = get_missions_a_affecter()
    missionsAffectes = get_missions_affectes()
    missionsClosed = get_missions_closes()
    return render_template('showmissions.html', missionsAAffecter=missionsAAffecter,
                           missionsAffectes=missionsAffectes,
                           missionsClosed=missionsClosed,
                           ingenieur_id=ingenieur_id)

@app.errorhandler(404)
def notFound(e):
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
