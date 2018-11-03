from flask import Flask, request, render_template
from service import *

app = Flask(__name__)
# app.secret_key = 'ytkey'

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # get data from html
        title = request.form["title"]
        description = request.form["description"]
        categories = request.form["categories"]
        date_saisie = datetime.date.today()

        if title == "" or description == "":
            print("No title or No description")

        # add mission in database
        addMission(title, description, categories)

        print("add successfully")
    return render_template('add.html')

@app.route('/showmissions',methods=['GET','POST'])
def showMissions():
    from database import db, Mission
    missions = Mission.query.all()
    return render_template('showmissions.html',missions=missions)


if __name__ == "__main__":
    from database import db
    print("creating database")
    db.drop_all()
    db.create_all()
    from test import *
    # test_db()
    # print("database created")
    # app.run()
