# PIL1_2425_25
Chaque année, l'Institut de Formation et de Recherche en Informatique (IFRI) incluent dans le programme universitaire un projet intégrateur visant à permettre aux étudiants de travailler sur un problème concret en groupe, leur permettant de proposer des solutions pratiques en se basant sur les enseignements reçus au cours de l'année.
Le projet de cette année  consiste à réaliser une application web de comotorage qui met  en relation des étudiants d'IFRI souhaitant partager leurs trajet quotidients entre leur domicile et le campus.

 A l'occasion de ce projet nous avons eu à créer GoVibe, une application de comotorage simple qui permet aux utilisateurs de proposer ou rechercher des trajets. Développée avec Django, HTML, CSS et JavaScript.
 
 # Fonctionnalités principales
 - Mise en place du système d'authentification (inscription, connexion, déconnexion, reinitialisation du mot de passe)
 - Fonctionnalités de demande de trajets
 - Recherche de trajets disponibles
 - Système de messagerie entre conducteurs et passager

 # Installation du projet
 1- Cloner le depôt:
```bash
       git clone https://github.com/ton_nom_utilisateur/PIL1_2425_25.git

2- Créer un environnement virtuel
````
   python -m venv env

3- Activer l'environnement virtuel
````    
    # Sous Windows :
    env\Scripts\activate   
    
    # Sous macOS / Linux :
    source env/bin/activate

4- Installer les dépendances
````
    pip install -r requirements.txt

5- Etre dans le dossier adéquat
````
    cd PIL1_2425_25\backend\comotorage    

6- Configurer la base de donnée dans le fichier setting.py:
````
   # Utilisation de MySQL:
    DATABASE = {
        'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'your_db_name',
        'USER' : 'your_db_user',
        'PASSWORD' : 'your_db_password'
        'HOST' : 'your_db_host', # Set to 'localhost' or '127.0.0.1' or local development
        'PORT' : '3306' # Port par défaut de mysql
        }
    }  

6- Appliquer les migrations
   # Une fois l’environnement virtuel activé et ta base de données prête :
`` 
   python manage.py makemigrations
   python manage.py migrate

6- Créer un super utilisateur
````
    python manage.py createsuperuse

7- Lancer le serveur de dévellopement et le serveur websocket  
````
    ./run_daphne.sh


# Technologies utilisées
- Python / Django
- HTML / CSS / JavaScript
- Git et GitHub