from pymongo import MongoClient, errors

class MongoDB:
    MONGO_URI = "mongodb+srv://mbowbayesaer44:UA4wH2MwIB4VGFyJ@cluster0.ipwzsvl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    def __init__(self):
        try:
            self.client = MongoClient(self.MONGO_URI)

            self.db = self.client["python"]
        except errors.ConnectionFailure as e:
            print("Erreur de connexion à MongoDB :", e)
            raise

    def get_collection(self, collection_name):
        return self.db[collection_name]

mongodb = MongoDB()
