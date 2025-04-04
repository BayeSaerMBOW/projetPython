from services.Etudiant import EtudiantService
from db.db import MongoDBClient
from db.redis_cache import RedisCache

def menu():
    # Initialisation des services
    MONGO_URI = "mongodb+srv://sidydiopbalde:Toubakhayra@clustergestionuserpytho.qm3bwmd.mongodb.net/etablissement?retryWrites=true&w=majority&appName=ClusterGestionUserPython"
    mongo_client = MongoDBClient(MONGO_URI, "etablissement")
    redis_cache = RedisCache()
    etudiant_service = EtudiantService(mongo_client, redis_cache)

    while True:
        print("\n1. Ajouter un étudiant")
        print("2. Afficher les étudiants")
        print("3. Quitter")
        
        choix = input("Votre choix : ")
        
        if choix == "1":
            nom = input("Nom : ")
            prenom = input("Prénom : ")
            telephone = input("Téléphone : ")
            classe = input("Classe : ")
            notes = list(map(int, input("Notes (séparées par des espaces) : ").split()))
            
            etudiant_service.ajouter_etudiant(nom, prenom, telephone, classe, notes)

        elif choix == "2":
            etudiants = etudiant_service.recuperer_etudiant()
            etudiant_service.afficher_etudiant(etudiants)

        elif choix == "3":
            print("Fermeture du programme...")
            break
        
        else:
            print("Choix invalide, veuillez réessayer.")

if __name__ == "__main__":
    menu()
