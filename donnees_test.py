import os
import random
import sqlite3
from datetime import date, timedelta

from werkzeug.security import generate_password_hash

DOSSIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(DOSSIER, "projet.db")

NOMS = [ 
    "Mbarga Jean-Pierre", "Ngo Bassa Colette", "Fotso Alphonse", "Atangana Rose",
    "Njoya Ibrahim", "Ekane Sandra", "Tchoupo Marcel", "Bello Moussa",
    "Kamga Hélène", "Nkoulou Pascal", "Mvondo Estelle", "Tagne Brice",
    "Ndongo Mireille", "Essomba Charles", "Fouda Yvette", "Kenmogne Aurélien",
    "Abena Solange", "Mballa Désiré", "Ngassa Pauline", "Wouapi Thierry",
    "Biyong Carine", "Tchinda Roland", "Onana Félicité", "Djoumessi Patrick",
    "Nana Laurette",
]
MONTANT = 10000           
NB_SEANCES = 25           
NB_PASSEES = 12           
NB_SANS_BENEFICIAIRE = 3 


def prochain_samedi(depuis):
    return depuis + timedelta(days=(5 - depuis.weekday()) % 7)


def remplir(db):
    auj = date.today()
    seance_13 = prochain_samedi(auj)     
    debut = seance_13 - timedelta(weeks=NB_PASSEES) 
    db.execute("INSERT INTO administrateurs (login, empreinte) VALUES (?, ?)",
               ("admin", generate_password_hash("Admin!2026")))
    for i, nom in enumerate(NOMS, start=1):
        role = "tresorier" if i == 1 else "president" if i == 2 else "membre"
        code = {"tresorier": "Tresor!2026", "president": "Pres!2026"}.get(role, "Membre!2026")
        adhesion = debut - timedelta(days=random.randint(10, 700))
        db.execute(
            "INSERT INTO membres (nom, telephone, date_adhesion, empreinte, role) "
            "VALUES (?, ?, ?, ?, ?)",
            (nom, f"6770000{i:02d}", adhesion.isoformat(), generate_password_hash(code), role))
    db.execute("INSERT INTO cycles (nom, montant_cotisation, periodicite, date_debut) "
               "VALUES (?, ?, 'hebdomadaire', ?)",
               ("Cycle 2026-2027", MONTANT, debut.isoformat()))
    ordre = list(range(1, len(NOMS) + 1))
    random.shuffle(ordre)                                  
    for n in range(1, NB_SEANCES + 1):
        beneficiaire = ordre[n - 1] if n <= NB_SEANCES - NB_SANS_BENEFICIAIRE else None
        db.execute("INSERT INTO seances (cycle_id, numero, date, beneficiaire_id) "
                   "VALUES (1, ?, ?, ?)",
                   (n, (debut + timedelta(weeks=n - 1)).isoformat(), beneficiaire))
    fiabilite = {i: random.choice([1.0, 0.97, 0.93, 0.85, 0.7]) for i in range(1, len(NOMS) + 1)}
    for n in range(1, NB_PASSEES + 1):
        jour = debut + timedelta(weeks=n - 1)
        for m in range(1, len(NOMS) + 1):
            if random.random() > fiabilite[m]:            
                if random.random() < 0.3:
                    db.execute("INSERT INTO penalites (membre_id, seance_id, motif, montant, payee) "
                               "VALUES (?, ?, 'absence', 1000, ?)", (m, n, int(random.random() < 0.4)))
                continue
            retard = 0 if random.random() < 0.8 else random.randint(1, 6)
            avance = 0 if retard else random.randint(0, 2)
            date_paiement = jour + timedelta(days=retard) - timedelta(days=avance)
            db.execute(
                "INSERT INTO cotisations (seance_id, membre_id, montant, date_paiement, mode) "
                "VALUES (?, ?, ?, ?, ?)",
                (n, m, MONTANT, date_paiement.isoformat(),
                 random.choice(["mobile_money", "mobile_money", "especes"])))
            if retard and random.random() < 0.6:
                db.execute("INSERT INTO penalites (membre_id, seance_id, motif, montant, payee) "
                           "VALUES (?, ?, 'retard', 500, ?)", (m, n, int(random.random() < 0.65)))
    for m in random.sample(range(1, len(NOMS) + 1), 9):
        db.execute("INSERT INTO cotisations (seance_id, membre_id, montant, date_paiement, mode) "
                   "VALUES (?, ?, ?, ?, ?)",
                   (NB_PASSEES + 1, m, MONTANT, auj.isoformat(),
                    random.choice(["mobile_money", "especes"])))
    db.execute("UPDATE seances SET montant_total = (SELECT COALESCE(SUM(montant), 0) "
               "FROM cotisations WHERE cotisations.seance_id = seances.id)")
    db.commit()

if __name__ == "__main__":
    random.seed(42)                
    if os.path.exists(BASE):
        os.remove(BASE)
    db = sqlite3.connect(BASE)
    db.execute("PRAGMA foreign_keys = ON")
    with open(os.path.join(DOSSIER, "schema.sql"), encoding="utf-8") as f:
        db.executescript(f.read())
    remplir(db)
    for table in ("administrateurs", "membres", "cycles", "seances", "cotisations", "penalites"):
        n = db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table} : {n} lignes")
    db.close()