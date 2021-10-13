Cette API est une application de CRM pour l'entreprise de gestion et conseil d'événements Epic Events

            -------------------------------------------------------------------------------

https://github.com/Pierre12412/CRM.git

Assurez vous d'avoir la version 3.9.4 de Python

Pour créer un environnement virtuel, lancez la commande suivante depuis répertoire : python -m venv virtualenv

Activez le ensuite avec la commande : virtualenv\Scripts\activate.bat

Puis récupérez les dépendances Python de requirements.txt avec la commande suivante : pip install -r requirements.txt

Enfin executez le programme en allant dans le fichier src : cd src

Vous devez posséder une base de donnée postgres version 13.4
Vous devez créer un fichier .env dans le dossier src\CRM et y inclure ces informations :
-----------------------------------------------------
SECRET_KEY = clé secrette django (vous pouvez en générer une sur : https://djecrety.ir/)
DEBUG = True/False

NAME = Nom de la base de donnée
USER = Utilisateur de la base de donnée
PASSWORD = Mot de passe de connexion de l'utilisateur
-----------------------------------------------------
Puis en tapant : python manage.py runserver

Le serveur de l'API étant lancé, vous pouvez maintenant faire vos appels à l'API en local

Lien de la documentation POSTMAN : https://documenter.getpostman.com/view/17600400/UV5TGfgG
