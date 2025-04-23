import csv
import os
import smtplib
from fpdf import FPDF
from db.mongodb import mongodb
from db.redis_cache import redis_cache
from models.etudiant import Etudiant
from services.SmsService import SmsService

class EtudiantService:
    def __init__(self):
        self.etudiants = mongodb.get_collection("etudiants")

    def ajouter_etudiant(self, etudiant):
        if self.etudiants.find_one({"telephone": etudiant.telephone}):
            print("❌ Étudiant déjà enregistré.")
            return

        if not all(0 <= note <= 20 for note in etudiant.notes):
            print("❌ Notes invalides.")
            return

        etudiant_dict = etudiant.to_dict()
        etudiant_dict["moyenne"] = sum(etudiant.notes) / len(etudiant.notes)
        self.etudiants.insert_one(etudiant_dict)
        etudiant_dict["_id"] = str(etudiant_dict["_id"])
        redis_cache.set_cache(f"etudiant:{etudiant.telephone}", etudiant_dict)
        print("✅ Étudiant ajouté avec succès.")

    def recuperer_etudiants(self):
        cache_keys = redis_cache.client.keys("etudiant:*")
        etudiants = [redis_cache.get_cache(key) for key in cache_keys]
        return etudiants or list(self.etudiants.find())

    def rechercher_etudiant(self, critere, valeur):
        return self.etudiants.find_one({critere: valeur})

    def calculer_moyenne_generale(self, classe):
        etudiants = self.etudiants.find({"classe": classe})
        moyennes = [sum(e["notes"]) / len(e["notes"]) for e in etudiants if e["notes"]]
        return sum(moyennes) / len(moyennes) if moyennes else 0

    def trier_etudiants_par_moyenne(self):
        etudiants = self.recuperer_etudiants()
        return sorted(etudiants, key=lambda e: e["moyenne"], reverse=True)[:10]

    def modifier_notes(self, telephone, notes):
        if not all(0 <= note <= 20 for note in notes):
            print("❌ Notes invalides.")
            return

        moyenne = sum(notes) / len(notes)
        self.etudiants.update_one(
            {"telephone": telephone},
            {"$set": {"notes": notes, "moyenne": moyenne}}
        )

        etudiant = self.rechercher_etudiant("telephone", telephone)
        if etudiant:
            redis_cache.set_cache(f"etudiant:{telephone}", etudiant)
            print("✅ Notes mises à jour.")
            self.envoyer_notification(etudiant["email"], "Vos notes ont été mises à jour.")
            if moyenne < 10:
                self.envoyer_notification(etudiant["email"], "⚠️ Votre moyenne est inférieure à 10/20.")

    def supprimer_etudiant(self, telephone):
        self.etudiants.delete_one({"telephone": telephone})
        redis_cache.delete_cache(f"etudiant:{telephone}")
        print("✅ Étudiant supprimé.")

    def exporter_csv(self, nom_fichier="etudiants.csv"):
        etudiants = self.recuperer_etudiants()
        if not etudiants:
            print("❌ Aucun étudiant à exporter.")
            return

        with open(nom_fichier, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nom", "prenom", "telephone", "classe", "notes", "moyenne"])
            writer.writeheader()
            for e in etudiants:
                writer.writerow({
                    "nom": e["nom"], "prenom": e["prenom"], "telephone": e["telephone"],
                    "classe": e["classe"], "notes": ", ".join(map(str, e["notes"])),
                    "moyenne": e["moyenne"]
                })
        print(f"✅ Export CSV : {nom_fichier}")

    def generer_rapport_pdf(self, nom_fichier="rapport_etudiants.pdf"):
        etudiants = self.recuperer_etudiants()
        if not etudiants:
            print("❌ Aucun étudiant à inclure.")
            return

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "Rapport des étudiants", ln=True, align="C")
        pdf.set_font("Arial", size=12)

        for e in etudiants:
            pdf.cell(0, 10, f"{e['nom']} {e['prenom']} - {e['classe']}", ln=True)
            pdf.cell(0, 10, f"Notes : {', '.join(map(str, e['notes']))}", ln=True)
            pdf.ln(5)

        pdf.output(nom_fichier)
        print(f"✅ Rapport PDF généré : {nom_fichier}")

    def envoyer_notification(self, email, message):
        try:
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            smtp_user = "sididiop53@gmail.com"
            smtp_pass = "mzfiinfxftbaafki"  # 🔒 À sécuriser avec .env

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_pass)
                server.sendmail(
                    smtp_user,
                    email.strip(),
                    f"From: {smtp_user}\r\nTo: {email}\r\nSubject: Notification\r\n\r\n{message}"
                )
            print(f"📨 Notification envoyée à {email}")
        except Exception as e:
            print(f"❌ Erreur d'envoi : {e}")


service_etudiant = EtudiantService()
