import redis
import json

class RedisCache:
    def __init__(self):
        try:
            # Connexion à Redis sur le port 6379
            self.client = redis.Redis(host="localhost", port=6379, decode_responses=True)
            self.client.ping()  # Vérifie que Redis est bien accessible
        except redis.ConnectionError as e:
            print("Erreur de connexion à Redis :", e)
            raise  # Remonte l'erreur si la connexion échoue

    def set_cache(self, key, value):
        # Sérialise (convertit) l'objet Python en JSON et le stocke dans Redis
        self.client.set(key, json.dumps(value))

    def get_cache(self, key):
        # Récupère la valeur depuis Redis et la désérialise en objet Python
        value = self.client.get(key)
        return json.loads(value) if value else None

    def delete_cache(self, key):
        # Supprime une clé du cache Redis
        self.client.delete(key)

# Création d'une instance globale accessible partout dans le projet
redis_cache = RedisCache()
