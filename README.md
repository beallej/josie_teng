# schema
mission
* id - INTEGER
* title - VARCHAR
* description - VARCHAR
* categories - ARRAY OF VARCHAR
* date_saisie - DATE
* date_affectue - DATE
* status - VARCHAR

souhaits
* id - INT
* voeux - VARCHAR
* mission_id - INTEGER (FK)
* ingenieur_etudes_id - INTEGER (FK)
* affectue - BOOL
* position_date - DATE

ingenieur_Etudes
* id - INT
