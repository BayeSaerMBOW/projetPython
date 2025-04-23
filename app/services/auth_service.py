import bcrypt
from db.mongodb import mongodb
from db.redis_sessions import redis_sessions
from models.user import User

class AuthService:
    def __init__(self):
        self.users = mongodb.get_collection("users")

    def inscrire_utilisateur(self, nom, email, password, role):
        if self.users.find_one({"email": email}):
            print("❌ Email déjà utilisé.")
            return

        if role not in ["admin", "enseignant", "etudiant"]:
            print("❌ Rôle invalide.")
            return

        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        utilisateur = User(nom, email, password_hash, role)
        self.users.insert_one(utilisateur.to_dict())
        print("✅ Utilisateur inscrit avec succès.")

    def connexion(self, email, password):
        user = self.users.find_one({"email": email})
        if not user:
            print("❌ Utilisateur introuvable.")
            return None

        if not bcrypt.checkpw(password.encode(), user["password"].encode()):
            print("❌ Mot de passe incorrect.")
            return None

        token = redis_sessions.create_session(user["email"], user["role"])
        print(f"✅ Connexion réussie ! Token : {token}")
        return token

    def verifier_session(self, token):
        return redis_sessions.get_session(token)

    def deconnexion(self, token):
        redis_sessions.delete_session(token)
        print("✅ Déconnexion réussie.")

# Instance globale
auth_service = AuthService()
