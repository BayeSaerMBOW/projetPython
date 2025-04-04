import json
import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379

class RedisCache:
    def __init__(self, host="localhost", port=6379):
        self.host = host
        self.port = port
        self.client = None

    def connect(self):
        """Établit la connexion à Redis."""
        try:
            self.client = redis.Redis(host=self.host, port=self.port, decode_responses=True)
            self.client.ping()  # Vérification de la connexion
            print("Connexion réussie à Redis")
        except redis.ConnectionError as e:
            print("Erreur de connexion à Redis :", e)
            raise

    def get_client(self):
        """Retourne l'objet Redis client."""
        if self.client is None:
            self.connect()
        return self.client

    def cache_student(self, telephone, etudiant):
        """Stocke un étudiant dans Redis sous forme de JSON."""
        try:
            if self.client is None:
                self.connect()
            cle_redis = f"etudiant:{telephone}"
            self.client.set(cle_redis, json.dumps(etudiant, default=str))
            print(f"Étudiant mis en cache dans Redis sous la clé {cle_redis}")
        except Exception as e:
            print("Erreur lors de la mise en cache dans Redis :", e)

