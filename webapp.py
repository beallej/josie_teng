import datetime

from flask import Flask, request, render_template

app = Flask(__name__)
app.secret_key = 'ytkey'

@app.route("/",methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # get data from html
        title = request.form["title"]
        description = request.form["description"]
        category = request.form["category"]
        date_saisie = datetime.date.today()

        if title == "" or description == "":
            print("No title or No description")

        # add mission in database
        from database import db, Mission
        new_mission = Mission()
        new_mission.title = title
        new_mission.description = description
        new_mission.category = category
        new_mission.date_saisie = date_saisie
        new_mission.status = ""
        # ingenieurs_positionnes
        # ingenieur_affectue
        db.session.add(new_mission)
        db.session.commit()
        print("add successfully")

    return render_template("index.html")

if __name__ == "__main__":
    # Create the DB
    from database import db
    print("creating database")
    db.create_all()
    print("database created")

    app.run()
