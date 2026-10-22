from app import app, get_db, cycle_courant, etat_cycle

with app.app_context():
    db = get_db()
    etat = etat_cycle(db, cycle_courant(db))
    k = etat["kpi"]
    p = etat["prochaine"]

    print("Membres actifs     :", etat["nb_membres"])
    print("Séances passées    :", k["seances_passees"], "/", k["seances_total"])
    print("Prochaine séance   : n°", p["numero"], p["date"],
          "| collecté :", p["collecte"], "/", p["attendu"])
    print("Total collecté     :", k["collecte_total"])
    print("Recouvrement       :", k["recouvrement"], "%")
    print("Total dû           :", k["total_du"], "FCFA,", k["nb_retardataires"], "retardataires")
    print("Pénalités impayées :", k["pen_impayees"], "FCFA")

    print("\n3 plus gros retardataires :")
    for i in etat["retardataires"][:3]:
        print("  ", i["nom"], "doit", i["du"], "| séances manquées :", i["manquantes"])

    print("\n3 membres les moins ponctuels :")
    for i in sorted(etat["membres"], key=lambda i: i["ponctualite"])[:3]:
        print("  ", i["nom"], i["ponctualite"], "%")