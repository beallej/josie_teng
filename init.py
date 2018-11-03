from flask import Flask, request, render_template

from service import create_account_pour_ingenieur_etudes, login

app = Flask(__name__)
app.secret_key = 'ytkey'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Login
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # get data from html
        username = request.form["username"]
        password = request.form["password"]
        if username == "" or password == "":
            print("No username or No password")
        else :
            ingenieur = login(username,password)
        if ingenieur != None :
            print("login success")
        else:
            print("login defeat")
    return render_template('login.html')

# Register
@app.route('/register',methods=['GET','POST'])
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
            create_account_pour_ingenieur_etudes(username,password,name)
            print("create account successful")
    return render_template('Register.html')

# @app.route('/add',methods=['GET','POST'])
# def add():
#     if request.method == 'POST':
#         # get data from html
#         title = request.form["title"]
#         description = request.form["description"]
#         categories = request.form["categories"]
#
#         if title == "" or description == "":
#             print("No title or No description")
#
#         # add mission in database
#         addMission(title, description, categories)
#
#         print("add successfully")
#     return render_template('add.html')

# @app.route('/showmissions',methods=['GET','POST'])
# def showMissions():
#     from database import db, Mission
#     missions = Mission.query.all()
#     return render_template('showmissions.html',missions=missions)


if __name__ == "__main__":
    # from database import db
    # print("creating database")
    # db.drop_all()
    # db.create_all()
    # from test import *
    #
    # # test_db()
    # # print("database created")
    app.jinja_env.auto_reload = True
    app.run()
