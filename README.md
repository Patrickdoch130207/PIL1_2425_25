
Chaque année, l'Institut de Formation et de Recherche en Informatique (IFRI) inclut dans le programme universitaire un projet intégrateur visant à permettre aux étudiants de travailler sur un problème concret en groupe, leur permettant de proposer des solutions pratiques en se basant sur les enseignements reçus au cours de l'année.

Le projet de cette année consiste à réaliser une application web de covoiturage qui met en relation des étudiants d'IFRI souhaitant partager leurs trajets quotidiens entre leur domicile et le campus.


À cette occasion, nous avons créé GoVibe, une application de covoiturage simple qui permet aux utilisateurs de proposer ou rechercher des trajets. Elle est développée avec Django, HTML, CSS et JavaScript.


---

Fonctionnalités principales

Système d'authentification (inscription, connexion, déconnexion, réinitialisation du mot de passe)

Création de demandes de trajets

Recherche de trajets disponibles

Système de messagerie entre conducteurs et passagers



---

Installation du projet

1. Cloner le dépôt

git clone https://github.com/ton_nom_utilisateur/PIL1_2425_25.git

2. Créer un environnement virtuel

python -m venv env

3. Activer l'environnement virtuel

# Sous Windows :
env\Scripts\activate

# Sous macOS / Linux :
source env/bin/activate

4. Installer les dépendances

pip install -r requirements.txt

5. Aller dans le dossier du projet

cd PIL1_2425_25/backend/comotorage

6. Configurer la base de données dans le fichier settings.py

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'your_db_host',  # 'localhost' ou '127.0.0.1' pour le développement local
        'PORT': '3306',  # Port par défaut de MySQL
    }
}

7. Appliquer les migrations

python manage.py makemigrations
python manage.py migrate

8. Créer un super utilisateur

python manage.py createsuperuser

9. Lancer le serveur de développement et le serveur WebSocket

./run_daphne.sh


---

Technologies utilisées

Python / Django

HTML / CSS / JavaScript

Git & GitHub



---

Souhaites-tu que je t’aide à ajouter des badges (ex : version, licence, état du projet) ou une capture d’écran de l’interface dans le README ?

