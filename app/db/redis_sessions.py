import redis
import uuid

class RedisSessions:
    def __init__(self):
        # Connexion à Redis avec décodage des réponses
        self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)

    def create_session(self, email, role):
        # Génère un token unique avec UUID
        token = str(uuid.uuid4())
  
        self.client.setex(f"session:{token}", 3600, f"{email},{role}")
        return token  # Retourne le token au client

    def get_session(self, token):
        # Récupère la session à partir du token
        session = self.client.get(f"session:{token}")
        if session:
            # Si la session existe, on la découpe en email et rôle
            email, role = session.split(",")
            return {"email": email, "role": role}
        return None  # Aucun résultat si la session est expirée ou inexistante

    def delete_session(self, token):
        # Supprime une session Redis
        self.client.delete(f"session:{token}")

# Instance globale utilisée dans le projet
redis_sessions = RedisSessions()
