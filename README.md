# schema
mission
* id - INTEGER
* title - VARCHAR
* description - VARCHAR
* categories - VARCHAR
* date_saisie - DATE
* date_closed - DATE
* status - VARCHAR

ingenieur_etudes
* id - INTEGER
* name - VARCHAR

positionnement
* voeux - VARCHAR
* mission_id - INTEGER (FK)
* ingenieur_etudes_id - INTEGER (FK)
* date_positione - DATE
* date_saisie - DATE

affectues
* mission_id - INTEGER (FK)
* ingenieur_etudes_id - INTEGER (FK)
* date_affectue - DATE


