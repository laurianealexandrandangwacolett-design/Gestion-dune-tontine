import re
import sqlite3

from app import app, BASE

app.config["TESTING"] = True
resultats = []


def verifier(description, condition):
    resultats.append(bool(condition))
    print(("OK     " if condition else "ECHEC  ") + description)


def jeton(client, url="/connexion"):
    """Lit le jeton CSRF caché dans une page."""
    html = client.get(url).get_data(as_text=True)
    m = re.search(r'name="csrf_token" value="([0-9a-f]+)"', html)
    return m.group(1) if m else ""


def connecter(identifiant, mot_de_passe):
    client = app.test_client()
    client.post("/connexion", data={"csrf_token": jeton(client),
                                    "identifiant": identifiant,
                                    "mot_de_passe": mot_de_passe})
    return client


print("--- Visiteur non connecté ---")
visiteur = app.test_client()
r = visiteur.get("/admin")
verifier("/admin redirige vers la connexion",
         r.status_code == 302 and "/connexion" in r.headers["Location"])
verifier("/admin/demandes redirige vers la connexion",
         visiteur.get("/admin/demandes").status_code == 302)
verifier("/mon-espace redirige vers la connexion", visiteur.get("/mon-espace").status_code == 302)
verifier("/api/statistiques répond 401", visiteur.get("/api/statistiques").status_code == 401)
verifier("/calendrier est public", visiteur.get("/calendrier").status_code == 200)
verifier("/rejoindre est public", visiteur.get("/rejoindre").status_code == 200)
verifier("/api/prochaine-seance est publique",
         visiteur.get("/api/prochaine-seance").status_code == 200)
r = visiteur.get("/page-inexistante")
verifier("page 404 personnalisée", r.status_code == 404 and "Page introuvable" in r.get_data(as_text=True))

print("\n--- Attaques ---")
r = visiteur.post("/connexion", data={"identifiant": "admin", "mot_de_passe": "x"})
verifier("POST de connexion sans jeton CSRF refusé (400)", r.status_code == 400)
r = visiteur.post("/rejoindre", data={"nom": "Test Nom", "telephone": "655999999"})
verifier("POST d'adhésion sans jeton CSRF refusé (400)", r.status_code == 400)

c = app.test_client()
r = c.post("/connexion", data={"csrf_token": jeton(c), "identifiant": "' OR '1'='1",
                               "mot_de_passe": "' OR '1'='1"})
verifier("injection SQL à la connexion refusée (401)", r.status_code == 401)
verifier("aucune session créée par l'injection", c.get("/admin").status_code == 302)

c = app.test_client()
r = c.post("/connexion", data={"csrf_token": jeton(c), "identifiant": "677000003",
                               "mot_de_passe": "Membre!2026", "suivant": "//evil.example"})
verifier("redirection vers un site extérieur bloquée",
         r.status_code == 302 and "evil" not in r.headers["Location"])

c = app.test_client()
t = jeton(c, "/rejoindre")
r = c.post("/rejoindre", data={"csrf_token": t, "nom": "Ab", "telephone": "123"})
verifier("demande d'adhésion invalide refusée (400)", r.status_code == 400)
r = c.post("/rejoindre", data={"csrf_token": t, "nom": "Paul Test", "telephone": "677000003"})
verifier("demande avec le numéro d'un membre refusée (400)", r.status_code == 400)

print("\n--- Membre simple ---")
membre = connecter("677000003", "Membre!2026")
verifier("/mon-espace accessible", membre.get("/mon-espace").status_code == 200)
verifier("/admin refusé (403)", membre.get("/admin").status_code == 403)
verifier("/admin/demandes refusé (403)", membre.get("/admin/demandes").status_code == 403)
verifier("/admin/penalites refusé (403)", membre.get("/admin/penalites").status_code == 403)
verifier("/api/statistiques refusé (403)", membre.get("/api/statistiques").status_code == 403)

print("\n--- Président (consultation seulement) ---")
pres = connecter("677000002", "Pres!2026")
verifier("/admin accessible", pres.get("/admin").status_code == 200)
verifier("/admin/demandes accessible", pres.get("/admin/demandes").status_code == 200)
t = jeton(pres, "/admin")
r = pres.post("/admin/penalites", data={"csrf_token": t, "membre_id": "1", "seance_id": "1",
                                        "motif": "retard", "montant": "500"})
verifier("enregistrer une pénalité refusé (403)", r.status_code == 403)
r = pres.post("/admin/seances/1/cotisations", data={"csrf_token": t, "date_paiement": "2026-01-01"})
verifier("enregistrer des cotisations refusé (403)", r.status_code == 403)
r = pres.post("/admin/demandes/1/accepter", data={"csrf_token": t, "code": "Abcdef1"})
verifier("accepter une demande d'adhésion refusé (403)", r.status_code == 403)

print("\n--- Trésorier ---")
tres = connecter("677000001", "Tresor!2026")
verifier("/admin accessible", tres.get("/admin").status_code == 200)
verifier("/admin/demandes accessible", tres.get("/admin/demandes").status_code == 200)
r = tres.get("/api/statistiques")
verifier("/api/statistiques renvoie du JSON",
         r.status_code == 200 and r.is_json and "retardataires" in r.get_json())

print("\n--- Données et configuration ---")
db = sqlite3.connect(BASE)
empreintes = [l[0] for l in db.execute(
    "SELECT empreinte FROM membres UNION ALL SELECT empreinte FROM administrateurs")]
verifier("tous les mots de passe sont hachés",
         all(e.startswith(("scrypt:", "pbkdf2:")) for e in empreintes))
source = open("app.py", encoding="utf-8").read()
verifier("debug=False dans app.py", "app.run(debug=True" not in source)

print(f"\n{sum(resultats)} / {len(resultats)} tests réussis")