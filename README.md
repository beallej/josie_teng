##Projet Maîtrise d'Oeuvre
#### Josie Bealle et Teng Yu

#### Pour avoir données initiales:
Dans `init.py` importez test.py. Initialize une instance de `UnitTests` et appelez sa methode setup avant d’appeler `app.run()`
```python
if __name__ == "__main__":
    from webapp.database import db
    from test.test import UnitTests
    u = UnitTests()
    u.setUp()
    db.create_all()
    app.jinja_env.auto_reload = True
    app.run()
```
Vous pouvez vous identifier avec les authentifiants suivants:
* `josieposie`, `password1` (Ingénieur d'Études)
* `felipemaple`, `password2` (Ingénieur d'Études)
* `pabloingles`, `password3` (Ingénieur d'Études)
* `adminaccount`, `password4` (Ingénieur d'Affaires)

Vouz pouvez filtrer par des catégories: `carriere`, `devoirs`, `francais`, `social`, `courses` ou des autres que vous avez ajouté a une mission

## Directories
####`static`
*  ####`img` : Ce dossier contient toutes les images du projet.
    *  `header.png` L'image affiché en haut de chaque page
* ####`style` : Ce dossier contient tous les styles de CSS qu'on a defini.
    * `style.css` Des styles qu'on a defini qui ne sont pas du Bootstrap
####`templates` Les templates visuels du projet. On a trouvé qu'il n'était pas nécessaire d'inclure `jinja2` dans le nom. La fonctionalité reste pareil.
* `404.html` : Quand le systèm ne marche pas bon ou le client fait quelques choses mal , la page va afficher cette `404.html` page. 
* `addmission.html` : Ce fichier est une page pour ajouter une nouvelle mission. L’information de la nouvelle mission include `titre`, `description`, `categories`.
* `ingenieur_affaires.html` : Ce fichier est une page du management pour le type d’ingénieur d’affaires. Toutes les missions(`Missions À Affecter`, `Missions Affectées`, `Missions Closes`) sont affiché avec les détails de la chaque mission. L’ingénieur d’affaire peut ajouter, supprimer ou clore la mission. De plus, il peut trouver le statut et l’information d’ingénieur d’études.
* `ingenieur_etudes.html` : Ce fichier est une page du management pour le type d’ingénieur d’études. L’ingénieur d’étude sélectionne la mission par catégories. Il peut insérer les voeux et positionner la mission. De plus, la fonction `Evolution d’activité` est pour afficher toutes les missions positionné par cet ingénieur d’étude.
* `ingenieur_evolution.html` : Cette page affiche les détails de toutes les missions qui concernent cet ingénieur d’étude. 
* `login.html` : Cette page est la homepage du systèm pour s’identifier. Le client peut entrer le  nom d’utilisateur , le mot de passe et choisir le type d’ingénieur. Pour le nouveau client le bouton sur s’inscrire tourne la page à `register.html`.
* `mission.html` : Cette page affiche le détail de la mission. L’ingénieur d’affaire peut trouver l’information sur `Ingénieur`, `Voeux`, `Date Positionné` et affecter cette mission.  
* `register.html` : Ce fichier est une page pour s’inscrire. Le client entre le nom d’utilisateur, le mot de passe, le type d’ingénieur, le prénom et le nom.
de passe, le prénom, le nom et le type d’ingénieur. Après vérifier l’information du nouveau compte tourner la page selon le type à `ingenieur_affaires.html` ou `ingenieur_etudes.html`.

####`test` Ce dossier contient des fichiers test pour le projet.
* `test.py` Ce fichier contient quelques testes unitaires pour le projet. 

####`webapp` Ce dossier contient des fichiers python pour le webapp sauf `init.py` qui est mieux placé dans le niveau le plus haut du projet
* `datapase.py` : Ce fichier contient le modèle de données… les tables dans le base de données, les relations entres les tables, etc.
* `dto.py`: Ce fichier transforme un objet ou des objet de la base de donnés en des objets plus utile pour le controlleur init.py à utiliser dans les templètes html.
* `service.py` Ce fichier extrait de l’information de la base de données selon des besoins du controlleur… et retourne cette information au controlleur. Par example, le controlleur demande à la service la liste des missions à affectuer.
* `utils.py` Ce fichier contient des fonctions qui peuvent aider plusieurs fichiers.. par example, convertir un date en string pour afficher.

**`init.py`**: Ce fichier est le controlleur, il definit des routes, il demande de l’information de la service selon des paramètres donnés et il rend des templetès avec cet information



`.gitignore` Ce fichier contient une liste de sorts de fichiers et dossiers à ne pas garder dans le repo github.

`README.md` Ce ficher contient de l'information sur le projet

`requirements.txt` Ce fichier definit quelques exigences de flask

`test.db` Ce fichier est le base de donnés






## Relations dans la base de donneés

#### Mission
* liste de ingenieurs positionnes (Positionnements) 	  	 	 		     	 	 	
* liste de ingenieurs affectues (Affectuation) 
* liste de Categories	  	 	 		     	 	 	

#### Categorie
* liste de Missions

#### Ingenieur (superclass)

#### Ingenieur_Affaires (subclass d'Ingenieur)

#### Ingenieur_Etudes (subclass d'Ingenieur)
* liste de missions positionnees (Positionnements)
* liste de missions affectuees (Affectuations)
 	  	 	 		     	 	 	
#### Action (superclass)

#### Positionnement (subclass d'Action)
* Mission
* Ingenieur_Etudes

#### Affectuation (subclass d'Action)
* Mission
* Ingenieur_Etudes

 	 		     	 	 		  	 	 		     	 	 	


