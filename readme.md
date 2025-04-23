🛠 Gestion_User_Python_POO_Mongo_Redis
Un projet Python pour gérer des utilisateurs avec une architecture orientée objet, utilisant MongoDB pour la persistance des données et Redis pour le cache.
🚀 Installation
🔹 Prérequis

Python 3.8+ : Assurez-vous que Python est installé (python3 --version).
MongoDB : Installez MongoDB Community Edition (Guide officiel).
Redis : Installez Redis (Guide officiel).
Git : Pour cloner le dépôt.

🔹 Étapes d'installation (Linux/macOS)

Clonez le dépôt :
git clone https://github.com/<votre-utilisateur>/Gestion_User_Python_POO_Mongo_Redis.git
cd Gestion_User_Python_POO_Mongo_Redis


Créez un environnement virtuel :
python3 -m venv venv


Activez l'environnement virtuel :
source venv/bin/activate


Installez les dépendances :
pip install -r requirements.txt


Démarrez le serveur MongoDB :Assurez-vous que MongoDB est installé et en cours d'exécution :
sudo systemctl start mongod

Vérifiez que MongoDB fonctionne :
mongo --eval "db.runCommand({ ping: 1 })"

Vous devriez voir une réponse avec "ok": 1.

Démarrez le serveur Redis :Assurez-vous que Redis est installé et en cours d'exécution :
sudo systemctl start redis

Vérifiez que Redis fonctionne :
redis-cli ping

Vous devriez voir PONG.


🔹 Étapes d'installation (Windows)

Clonez le dépôt :

Utilisez Git Bash ou un client Git pour cloner :git clone https://github.com/<votre-utilisateur>/Gestion_User_Python_POO_Mongo_Redis.git
cd Gestion_User_Python_POO_Mongo_Redis




Créez un environnement virtuel :
python -m venv venv


Activez l'environnement virtuel :
venv\Scripts\activate


Installez les dépendances :
pip install -r requirements.txt


Démarrez le serveur MongoDB :

Installez MongoDB Community Edition pour Windows (Guide officiel).
Lancez MongoDB (si configuré comme service) :net start MongoDB


Vérifiez avec :mongo --eval "db.runCommand({ ping: 1 })"




Démarrez le serveur Redis :

Installez Redis pour Windows (par exemple, via WSL ou une version non officielle comme Microsoft Archive).
Lancez Redis manuellement (si non configuré comme service) :redis-server


Vérifiez avec :redis-cli ping

Vous devriez voir PONG.



📌 Configuration

Fichier .env :Créez un fichier .env à la racine du projet pour configurer les connexions à MongoDB et Redis. Exemple :
MONGO_URI=mongodb://localhost:27017/gestion_users
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0

Ajustez selon votre configuration.

Mettez à jour config.py :Assurez-vous que app/utils/config.py charge ces variables d'environnement (par exemple, avec python-dotenv).


📂 Structure du projet
Gestion_User_Python_POO_Mongo_Redis/
│── app/
│   ├── models/
│   │   ├── user.py
│   ├── services/
│   │   ├── user_service.py
│   ├── repositories/
│   │   ├── mongo_repository.py
│   │   ├── redis_repository.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── logger.py
│   ├── routes/
│   ├── main.py
│
├── tests/
│   ├── test_user_service.py
├── .env
├── requirements.txt
├── README.md

🔧 Dépendances
Les dépendances sont listées dans requirements.txt. Voici les principales :
pymongo==4.12.0
redis==5.2.1
python-dotenv==1.0.1

Pour générer un nouveau requirements.txt :
pip freeze > requirements.txt

🚀 Utilisation

Assurez-vous que MongoDB et Redis sont en cours d'exécution :
sudo systemctl status mongod
sudo systemctl status redis


Lancez l'application :
python3 app/main.py


Testez les fonctionnalités :

Ajoutez un utilisateur via user_service.py, qui stocke les données dans MongoDB et met en cache certaines informations dans Redis.
Exemple d'interaction :from app.services.user_service import UserService
service = UserService()
service.create_user({"name": "Bobo Sow", "email": "bobo@example.com"})





🧪 Tests

Installez les dépendances de test (si nécessaire, par exemple pytest) :
pip install pytest


Exécutez les tests :
pytest tests/



⚠️ Résolution des problèmes

Erreur de connexion MongoDB :

Vérifiez que MongoDB est en cours d'exécution (sudo systemctl status mongod).
Confirmez que MONGO_URI dans .env est correct.


Erreur de connexion Redis :

Vérifiez que Redis est en cours d'exécution (redis-cli ping).
Assurez-vous que REDIS_HOST et REDIS_PORT dans .env sont corrects.
Si le port 6379 est occupé :sudo lsof -i :6379
sudo kill -9 <PID>




Dépendances manquantes :
pip install -r requirements.txt



