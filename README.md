# schema
mission
* id - INTEGER
* title - VARCHAR
* description - VARCHAR
* categories - ARRAY OF VARCHAR
* date_saisie - DATE
* date_closed - DATE
* status - VARCHAR

souhaits
* id - INT
* voeux - VARCHAR
* mission_id - INTEGER (FK)
* ingenieur_etudes_id - INTEGER (FK)
* position_date - DATE

affectues
* id - INT
* mission_id - INTEGER (FK)
* ingenieur_etudes_id - INTEGER (FK)
* date_affectue - DATE

ingenieur_etudes
* id - INT
