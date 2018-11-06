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




#Idea for structure
`/` homepage
* link to login ingenieur d'etudes (`/login/ingenieur_etudes` )
* link to login ingenier d'affaires (`/login/ingenieur_affaires` ) 
* link to create account (`/account/create`)

`/login/ingenieur_etudes` login for ingenieur d'etudes
* on submission redirects to `/user/<id> `
* link to home (`/`)

`/login/ingenieur_affaires` login for ingenieur d'affaires
* on submission redirects to `/user/<id> `
* link to home(`/`)

`/account/create` create account
* on submission redirects to `/user/<id> `
* link to home(`/`)

`/user/<id> ` page for an ingenieur. should be different for different types
* If Ingenieur d'Affaires:
    * Button to create mission that submits  POST request to `/mission/create`
    * For each mission:
        * option to add ingenieur d'etudes and button to affectuer the mission, which submists PUT request to `/mission/affectuer` with the ingenieur d'etudes in the body of the request
        * option to "cloire" mission by submitting PUT request to `/mission/cloire`
        * option to "supprimer" mission by submitting DELETE request to `mission/delete`
    
* If Ingenieur d'Etudes:
    * For each mission that is "a affecter", option to add "Voeux" and Positionner for the mission submitting POST to `/mission/positionner` with the voeux and the id of the ingenieur d'etudes in the body of the request
* link to home(`/`)



