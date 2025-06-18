

# Stop script if any command fails
set -e

# Démarrer Redis en arrière-plan (si installé localement)
echo "🔄 Lancement de Redis..."
redis-server --daemonize yes

# Exporter les variables d'environnement nécessaires à Django
export DJANGO_SETTINGS_MODULE=comotorage.settings
# Lancement du serveur Django (8000)
echo "🚀 Lancement de Django sur 8000..."
python manage.py runserver &
# Lancer Daphne sur 127.0.0.1:8001
echo "🚀 Lancement de Daphne sur le port 8001..."
daphne -b 127.0.0.1 -p 8001 comotorage.asgi:application

