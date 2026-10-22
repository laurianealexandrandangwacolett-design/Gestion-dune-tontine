import os
import re
import secrets
import sqlite3
from datetime import date
from functools import wraps

from flask import (Flask, abort, flash, g, jsonify, redirect, render_template,
                   request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash

DOSSIER = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(DOSSIER, "projet.db")
NOM_ASSOCIATION = "Tontine Union & Solidarité"
HEURE_SEANCE = "16:00"          

GESTION = ("admin", "tresorier")                    
CONSULTATION = ("admin", "tresorier", "president")  

MODES = {"especes": "Espèces", "mobile_money": "Mobile money"}
MOTIFS = {"retard": "Retard", "absence": "Absence"}
ROLES = {"membre": "Membre", "tresorier": "Trésorier", "president": "Président"}
RE_TEL = re.compile(r"6\d{8}")      

app = Flask(__name__)
app.config["SECRET_KEY"] = "changez-moi-tontine-groupe09"

def get_db():
    """Une connexion par requête, clés étrangères activées."""
    if "db" not in g:
        g.db = sqlite3.connect(BASE)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def fermer_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin",
        "juil.", "août", "sept.", "oct.", "nov.", "déc."]
JOURS = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
PALETTE = ["#0F5C46", "#B5472F", "#B7791F", "#2F6F9F", "#7A4E9E",
           "#17805F", "#A63D6E", "#4F7A28"]


@app.template_filter("fcfa")
def filtre_fcfa(valeur):
    """10000 -> « 10 000 FCFA »."""
    return f"{int(valeur or 0):,}".replace(",", "\u202f") + "\u00a0FCFA"


@app.template_filter("date_fr")
def filtre_date(iso, long=False):
    """'2026-10-17' -> '17 oct. 2026' (ou 'samedi 17 oct. 2026' avec long=True)."""
    if not iso:
        return "—"
    d = date.fromisoformat(iso)
    court = f"{d.day} {MOIS[d.month - 1]} {d.year}"
    return f"{JOURS[d.weekday()]} {court}" if long else court


@app.template_filter("initiales")
def filtre_initiales(nom):
    """'Fotso Alphonse' -> 'FA' (pour les avatars)."""
    mots = [m for m in (nom or "?").split() if m]
    return (mots[0][0] + (mots[1][0] if len(mots) > 1 else "")).upper()


@app.template_filter("couleur")
def filtre_couleur(nom):
    """Une couleur stable pour chaque nom."""
    return PALETTE[sum(ord(c) for c in (nom or "")) % len(PALETTE)]


@app.context_processor
def contexte_global():
    u = session.get("utilisateur")
    nb_demandes = 0
    if u and u["role"] in CONSULTATION:           
        try:
            nb_demandes = get_db().execute(
                "SELECT COUNT(*) FROM demandes_adhesion WHERE statut = 'en_attente'"
            ).fetchone()[0]
        except sqlite3.OperationalError:          
            nb_demandes = 0
    return {
        "association": NOM_ASSOCIATION,
        "utilisateur": u,
        "peut_gerer": bool(u and u["role"] in GESTION),
        "peut_consulter": bool(u and u["role"] in CONSULTATION),
        "MODES": MODES, "MOTIFS": MOTIFS, "ROLES": ROLES,
        "aujourdhui": date.today().isoformat(),
        "nb_demandes": nb_demandes,
    }

def jeton_csrf():
    """Un jeton secret par session, caché dans chaque formulaire POST."""
    if "csrf" not in session:
        session["csrf"] = secrets.token_hex(16)
    return session["csrf"]


app.jinja_env.globals["csrf_token"] = jeton_csrf


@app.before_request
def verifier_csrf():
    """Un POST sans le bon jeton est refusé : un site pirate ne peut pas l'envoyer à ta place."""
    if request.method == "POST":
        envoye = request.form.get("csrf_token") or request.headers.get("X-CSRF-Token", "")
        if not envoye or not secrets.compare_digest(envoye, session.get("csrf", "")):
            abort(400)


@app.after_request
def entetes_securite(reponse):
    reponse.headers["X-Content-Type-Options"] = "nosniff"
    reponse.headers["X-Frame-Options"] = "SAMEORIGIN"
    reponse.headers["Referrer-Policy"] = "same-origin"
    return reponse


def chemin_sur(chemin):
    """N'accepte qu'une adresse interne (empêche une redirection vers un site pirate)."""
    if chemin and chemin.startswith("/") and not chemin.startswith("//"):
        return chemin
    return None


def connexion_requise(f):
    """Réserve une route aux personnes connectées."""
    @wraps(f)
    def interne(*args, **kwargs):
        if not session.get("utilisateur"):
            flash("Connectez-vous pour accéder à cette page.", "erreur")
            return redirect(url_for("connexion", suivant=request.path))
        return f(*args, **kwargs)
    return interne

def role_requis(*roles):
    """Réserve une route à certains rôles : @role_requis('admin', 'tresorier')."""
    def decorateur(f):
        @wraps(f)
        def interne(*args, **kwargs):
            u = session.get("utilisateur")
            if not u:
                flash("Connectez-vous pour accéder à cette page.", "erreur")
                return redirect(url_for("connexion", suivant=request.path))
            if u["role"] not in roles:
                abort(403)
            return f(*args, **kwargs)
        return interne
    return decorateur


def api_role_requis(*roles):
    """Comme role_requis, mais répond en JSON (401 ou 403) au lieu de rediriger."""
    def decorateur(f):
        @wraps(f)
        def interne(*args, **kwargs):
            u = session.get("utilisateur")
            if not u:
                return jsonify(erreur="Connexion requise."), 401
            if u["role"] not in roles:
                return jsonify(erreur="Accès refusé."), 403
            return f(*args, **kwargs)
        return interne
    return decorateur


def sans_cache(reponse):
    """Empêche le navigateur de garder une vieille réponse."""
    reponse.headers["Cache-Control"] = "no-store"
    return reponse

def cycle_courant(db):
    """Le cycle le plus récent."""
    return db.execute(
        "SELECT * FROM cycles ORDER BY date_debut DESC, id DESC LIMIT 1").fetchone()


def etat_cycle(db, cycle):
    """Calcule tout ce que les pages affichent : séances, retards, ponctualité, pénalités."""
    auj = date.today().isoformat()
    montant = cycle["montant_cotisation"]

    membres = db.execute(
        "SELECT id, nom, telephone, role, date_adhesion FROM membres "
        "WHERE actif = 1 ORDER BY nom").fetchall()
    nb_membres = len(membres)
    attendu = nb_membres * montant           

    seances_bd = db.execute(
        "SELECT s.id, s.numero, s.date, s.beneficiaire_id, m.nom AS beneficiaire_nom "
        "FROM seances s LEFT JOIN membres m ON m.id = s.beneficiaire_id "
        "WHERE s.cycle_id = ? ORDER BY s.numero", (cycle["id"],)).fetchall()
    cotis = db.execute(
        "SELECT c.id, c.seance_id, c.membre_id, c.montant, c.date_paiement, c.mode "
        "FROM cotisations c JOIN seances s ON s.id = c.seance_id "
        "WHERE s.cycle_id = ?", (cycle["id"],)).fetchall()
    pens = db.execute(
        "SELECT p.id, p.membre_id, p.seance_id, p.motif, p.montant, p.payee, "
        "s.numero, mb.nom AS membre_nom "
        "FROM penalites p JOIN seances s ON s.id = p.seance_id "
        "JOIN membres mb ON mb.id = p.membre_id "
        "WHERE s.cycle_id = ? ORDER BY s.numero DESC, mb.nom", (cycle["id"],)).fetchall()
    par_seance = {}
    for c in cotis:
        par_seance.setdefault(c["seance_id"], {})[c["membre_id"]] = c
    seances, prochaine = [], None
    for s in seances_bd:
        payes = par_seance.get(s["id"], {})
        collecte = sum(c["montant"] for c in payes.values())
        info = {
            "id": s["id"], "numero": s["numero"], "date": s["date"],
            "passee": s["date"] < auj, "aujourdhui": s["date"] == auj,
            "beneficiaire_id": s["beneficiaire_id"],
            "beneficiaire_nom": s["beneficiaire_nom"],
            "collecte": collecte, "attendu": attendu,
            "nb_payes": len(payes), "nb_attendus": nb_membres,
            "taux": min(100, round(100 * collecte / attendu)) if attendu else 0,
        }
        seances.append(info)
        if prochaine is None and not info["passee"]:
            prochaine = info                 
    for info in seances:
        info["statut"] = ("passee" if info["passee"]
                          else "prochaine" if info is prochaine else "avenir")

    passees = [s for s in seances if s["passee"]]
    seance_de = {s["beneficiaire_id"]: s for s in seances if s["beneficiaire_id"]}
    infos = []
    for m in membres:
        dues = [s for s in passees if s["date"] >= m["date_adhesion"]]
        manquantes, ponctuelles, payees = [], 0, 0
        for s in dues:
            c = par_seance.get(s["id"], {}).get(m["id"])
            if c is None:
                manquantes.append(s["numero"])           
            else:
                payees += 1
                if c["date_paiement"] <= s["date"]:
                    ponctuelles += 1
        mes_pens = [p for p in pens if p["membre_id"] == m["id"]]
        infos.append({
            "id": m["id"], "nom": m["nom"], "telephone": m["telephone"],
            "role": m["role"], "date_adhesion": m["date_adhesion"],
            "manquantes": manquantes, "du": len(manquantes) * montant,
            "payees_passees": payees,
            "ponctualite": round(100 * ponctuelles / len(dues)) if dues else 100,
            "nb_dues": len(dues),
            "nb_pen": len(mes_pens),
            "pen_total": sum(p["montant"] for p in mes_pens),
            "pen_impayees": sum(p["montant"] for p in mes_pens if not p["payee"]),
            "seance_benefice": seance_de.get(m["id"]),
        })
    collecte_total = sum(s["collecte"] for s in seances)
    collecte_passees = sum(s["collecte"] for s in passees)
    attendu_passees = len(passees) * attendu
    retardataires = sorted((i for i in infos if i["du"] > 0), key=lambda i: -i["du"])
    return {
        "cycle": dict(cycle), "montant": montant, "nb_membres": nb_membres,
        "attendu": attendu, "seances": seances, "prochaine": prochaine,
        "membres": infos, "par_id": {i["id"]: i for i in infos},
        "retardataires": retardataires, "penalites": pens, "par_seance": par_seance,
        "deja_beneficiaires": {s["beneficiaire_id"] for s in seances if s["beneficiaire_id"]},
        "kpi": {
            "collecte_total": collecte_total,
            "attendu_passees": attendu_passees,
            "recouvrement": min(100, round(100 * collecte_passees / attendu_passees))
                            if attendu_passees else 100,
            "nb_retardataires": len(retardataires),
            "total_du": sum(i["du"] for i in retardataires),
            "pen_impayees": sum(p["montant"] for p in pens if not p["payee"]),
            "pen_total": sum(p["montant"] for p in pens),
            "seances_passees": len(passees), "seances_total": len(seances),
            "progression": round(100 * len(passees) / len(seances)) if seances else 0,
        },
    }


def charger_etat():
    """Renvoie (db, état du cycle courant), ou une erreur 503 si la base est vide."""
    db = get_db()
    cycle = cycle_courant(db)
    if cycle is None:
        abort(503)
    return db, etat_cycle(db, cycle)


def peut_gerer():
    """Vrai si l'utilisateur connecté a le droit d'enregistrer de l'argent."""
    u = session.get("utilisateur")
    return bool(u and u["role"] in GESTION)


def entier(texte, minimum=None, maximum=None):
    """Convertit un texte en entier, ou renvoie None s'il est invalide ou hors bornes."""
    texte = (texte or "").strip()
    if not texte.isdigit():
        return None
    n = int(texte)
    if (minimum is not None and n < minimum) or (maximum is not None and n > maximum):
        return None
    return n


def date_valide(texte):
    """Convertit '2026-10-17' en date, ou renvoie None."""
    try:
        return date.fromisoformat(texte or "")
    except ValueError:
        return None


def recalculer_total(db, id_seance):
    """Garde seances.montant_total égal à la somme des cotisations."""
    db.execute(
        "UPDATE seances SET montant_total = (SELECT COALESCE(SUM(montant), 0) "
        "FROM cotisations WHERE seance_id = ?) WHERE id = ?", (id_seance, id_seance))

@app.route("/")
def accueil():
    _, etat = charger_etat()
    return render_template("index.html", etat=etat)


@app.route("/calendrier")
def calendrier():
    _, etat = charger_etat()
    return render_template("calendrier.html", etat=etat)

@app.route("/rejoindre", methods=["GET", "POST"])
def rejoindre():
    """Demande d'adhésion faite par un visiteur (le trésorier l'accepte ou la refuse)."""
    donnees = {}
    if request.method == "POST":
        db = get_db()
        nom = " ".join(request.form.get("nom", "").split())
        tel = request.form.get("telephone", "").replace(" ", "")
        message = request.form.get("message", "").strip()
        donnees = {"nom": nom, "telephone": tel, "message": message}

        erreurs = []
        if not 3 <= len(nom) <= 80:
            erreurs.append("Le nom doit contenir entre 3 et 80 caractères.")
        if not RE_TEL.fullmatch(tel):
            erreurs.append("Téléphone invalide : 9 chiffres commençant par 6.")
        if len(message) > 300:
            erreurs.append("Le message ne doit pas dépasser 300 caractères.")

        if not erreurs:
            deja = (db.execute("SELECT 1 FROM membres WHERE telephone = ? AND actif = 1",
                               (tel,)).fetchone()
                    or db.execute("SELECT 1 FROM demandes_adhesion "
                                  "WHERE telephone = ? AND statut = 'en_attente'",
                                  (tel,)).fetchone())
            nb_attente = db.execute("SELECT COUNT(*) FROM demandes_adhesion "
                                    "WHERE statut = 'en_attente'").fetchone()[0]
            if deja:
                erreurs.append("Cette demande ne peut pas être enregistrée : ce numéro "
                               "est déjà membre ou une demande est déjà en cours.")
            elif nb_attente >= 50:                # limite anti-abus sur une page publique
                erreurs.append("Trop de demandes en attente pour le moment. "
                               "Réessayez plus tard.")

        if erreurs:
            for e in erreurs:
                flash(e, "erreur")
            return render_template("rejoindre.html", donnees=donnees), 400

        try:
            db.execute("INSERT INTO demandes_adhesion (nom, telephone, message, date_demande) "
                       "VALUES (?, ?, ?, ?)",
                       (nom, tel, message or None, date.today().isoformat()))
            db.commit()
        except sqlite3.IntegrityError:            
            flash("Une demande est déjà en cours pour ce numéro.", "erreur")
            return render_template("rejoindre.html", donnees=donnees), 400
        flash("Votre demande a été envoyée. Le trésorier la examinera et vous contactera.",
              "succes")
        return redirect(url_for("rejoindre"))

    return render_template("rejoindre.html", donnees=donnees)

@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    suivant = chemin_sur(request.values.get("suivant", ""))
    if request.method == "POST":
        identifiant = request.form.get("identifiant", "").strip()
        mot_de_passe = request.form.get("mot_de_passe", "")
        db = get_db()
        utilisateur = None
        adm = db.execute("SELECT * FROM administrateurs WHERE login = ?",
                         (identifiant,)).fetchone()
        if adm and check_password_hash(adm["empreinte"], mot_de_passe):
            utilisateur = {"type": "admin", "id": adm["id"],
                           "nom": adm["login"], "role": "admin"}
        else:
            tel = identifiant.replace(" ", "")
            m = db.execute("SELECT * FROM membres WHERE telephone = ? AND actif = 1",
                           (tel,)).fetchone()
            if m and check_password_hash(m["empreinte"], mot_de_passe):
                utilisateur = {"type": "membre", "id": m["id"],
                               "nom": m["nom"], "role": m["role"]}

        if utilisateur is None:
            flash("Identifiant ou mot de passe incorrect.", "erreur")
            return render_template("connexion.html", identifiant=identifiant,
                                   suivant=suivant), 401

        session.clear()                       
        session["utilisateur"] = utilisateur
        flash(f"Bienvenue, {utilisateur['nom']} !", "succes")
        if suivant:
            return redirect(suivant)
        if utilisateur["role"] in CONSULTATION:
            return redirect(url_for("tableau_bord"))
        return redirect(url_for("mon_espace"))

    if session.get("utilisateur"):
        return redirect(url_for("mon_espace"))
    return render_template("connexion.html", identifiant="", suivant=suivant)


@app.route("/deconnexion", methods=["POST"])
def deconnexion():
    session.clear()
    flash("Vous êtes déconnecté. À bientôt !", "info")
    return redirect(url_for("accueil"))

@app.route("/mon-espace")
@connexion_requise
def mon_espace():
    u = session["utilisateur"]
    if u["type"] != "membre":                 
        return redirect(url_for("tableau_bord"))
    _, etat = charger_etat()
    moi = etat["par_id"].get(u["id"])
    if moi is None:
        abort(404)
    lignes = []                                
    for s in etat["seances"]:
        c = etat["par_seance"].get(s["id"], {}).get(u["id"])
        if c:
            etat_ligne = "ponctuel" if c["date_paiement"] <= s["date"] else "tardif"
        else:
            etat_ligne = "retard" if s["passee"] else "avenir"
        lignes.append({"seance": s, "cotisation": c, "etat": etat_ligne})
    mes_pens = [p for p in etat["penalites"] if p["membre_id"] == u["id"]]
    return render_template("mon_espace.html", etat=etat, moi=moi,
                           lignes=lignes, mes_pens=mes_pens)


@app.route("/mon-espace/code", methods=["POST"])
@connexion_requise
def changer_code():
    u = session["utilisateur"]
    if u["type"] != "membre":
        abort(403)
    db = get_db()
    m = db.execute("SELECT * FROM membres WHERE id = ?", (u["id"],)).fetchone()
    ancien = request.form.get("ancien", "")
    nouveau = request.form.get("nouveau", "")
    confirmation = request.form.get("confirmation", "")
    if not m or not check_password_hash(m["empreinte"], ancien):
        flash("L'ancien code d'accès est incorrect.", "erreur")
    elif len(nouveau) < 6:
        flash("Le nouveau code doit contenir au moins 6 caractères.", "erreur")
    elif nouveau != confirmation:
        flash("La confirmation ne correspond pas au nouveau code.", "erreur")
    else:
        db.execute("UPDATE membres SET empreinte = ? WHERE id = ?",
                   (generate_password_hash(nouveau), u["id"]))
        db.commit()
        flash("Votre code d'accès a été modifié.", "succes")
    return redirect(url_for("mon_espace"))

@app.route("/admin")
@role_requis(*CONSULTATION)
def tableau_bord():
    _, etat = charger_etat()
    return render_template("admin/tableau_bord.html", etat=etat)


@app.route("/admin/seances")
@role_requis(*CONSULTATION)
def admin_seances():
    _, etat = charger_etat()
    nb_sans_benef = len([s for s in etat["seances"] if not s["beneficiaire_id"]])
    nb_sans_tour = len([m for m in etat["membres"] if m["id"] not in etat["deja_beneficiaires"]])
    return render_template("admin/seances.html", etat=etat,
                           nb_sans_benef=nb_sans_benef, nb_sans_tour=nb_sans_tour)

@app.route("/admin/seances/<int:id_seance>/beneficiaire", methods=["POST"])
@role_requis(*GESTION)
def designer_beneficiaire(id_seance):
    db = get_db()
    seance = db.execute("SELECT * FROM seances WHERE id = ?", (id_seance,)).fetchone()
    if seance is None:
        abort(404)
    choix = request.form.get("beneficiaire", "")
    if choix == "":                                   
        db.execute("UPDATE seances SET beneficiaire_id = NULL WHERE id = ?", (id_seance,))
        db.commit()
        flash(f"Séance n°{seance['numero']} : bénéficiaire retiré.", "info")
        return redirect(url_for("admin_seances"))
    id_membre = entier(choix)
    membre = db.execute("SELECT * FROM membres WHERE id = ? AND actif = 1",
                        (id_membre,)).fetchone() if id_membre else None
    if membre is None:
        flash("Membre inconnu.", "erreur")
        return redirect(url_for("admin_seances"))
    autre = db.execute(
        "SELECT numero FROM seances WHERE cycle_id = ? AND beneficiaire_id = ? AND id != ?",
        (seance["cycle_id"], id_membre, id_seance)).fetchone()
    if autre:
        flash(f"{membre['nom']} bénéficie déjà à la séance n°{autre['numero']} : "
              "un membre ne bénéficie qu'une fois par cycle.", "erreur")
        return redirect(url_for("admin_seances"))
    db.execute("UPDATE seances SET beneficiaire_id = ? WHERE id = ?", (id_membre, id_seance))
    db.commit()
    flash(f"Séance n°{seance['numero']} : {membre['nom']} est désigné(e) bénéficiaire.", "succes")
    return redirect(url_for("admin_seances"))


@app.route("/admin/cycles/<int:id_cycle>/tirage", methods=["POST"])
@role_requis(*GESTION)
def tirage_au_sort(id_cycle):
    """Attribue au hasard les séances sans bénéficiaire aux membres qui n'ont pas encore leur tour."""
    db = get_db()
    seances = db.execute(
        "SELECT id FROM seances WHERE cycle_id = ? AND beneficiaire_id IS NULL "
        "ORDER BY numero", (id_cycle,)).fetchall()
    candidats = [r["id"] for r in db.execute(
        "SELECT id FROM membres WHERE actif = 1 AND id NOT IN "
        "(SELECT beneficiaire_id FROM seances WHERE cycle_id = ? "
        "AND beneficiaire_id IS NOT NULL)", (id_cycle,)).fetchall()]
    secrets.SystemRandom().shuffle(candidats)
    n = min(len(seances), len(candidats))
    for s, id_membre in zip(seances[:n], candidats[:n]):
        db.execute("UPDATE seances SET beneficiaire_id = ? WHERE id = ?", (id_membre, s["id"]))
    db.commit()
    if n:
        flash(f"Tirage au sort effectué : {n} bénéficiaire(s) désigné(s).", "succes")
    else:
        flash("Rien à tirer : toutes les séances ont déjà un bénéficiaire.", "info")
    return redirect(url_for("admin_seances"))


@app.route("/admin/seances/<int:id_seance>/cotisations", methods=["GET", "POST"])
@role_requis(*CONSULTATION)
def cotisations_seance(id_seance):
    db, etat = charger_etat()
    seance = next((s for s in etat["seances"] if s["id"] == id_seance), None)
    if seance is None:
        abort(404)

    if request.method == "POST":
        if not peut_gerer():
            abort(403)                                
        jour = date_valide(request.form.get("date_paiement", ""))
        if jour is None or jour > date.today():
            flash("Date de paiement invalide (elle ne peut pas être dans le futur).", "erreur")
            return redirect(url_for("cotisations_seance", id_seance=id_seance))
        enregistres = 0
        for brut in request.form.getlist("membre"):   
            id_membre = entier(brut)
            membre = db.execute("SELECT id FROM membres WHERE id = ? AND actif = 1",
                                (id_membre,)).fetchone() if id_membre else None
            mode = request.form.get(f"mode_{brut}", "")
            if membre is None or mode not in MODES:
                continue
            try:
                db.execute(
                    "INSERT INTO cotisations (seance_id, membre_id, montant, date_paiement, mode) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (id_seance, id_membre, etat["montant"], jour.isoformat(), mode))
                enregistres += 1
            except sqlite3.IntegrityError:
                pass                                  
        recalculer_total(db, id_seance)
        db.commit()
        if enregistres:
            total = f"{enregistres * etat['montant']:,}".replace(",", "\u202f")
            flash(f"{enregistres} cotisation(s) enregistrée(s) ({total} FCFA).", "succes")
        else:
            flash("Aucune cotisation enregistrée : cochez au moins un membre.", "info")
        return redirect(url_for("cotisations_seance", id_seance=id_seance))

    payes = etat["par_seance"].get(id_seance, {})
    lignes = [{"membre": m, "cotisation": payes.get(m["id"])} for m in etat["membres"]]
    return render_template("admin/cotisations.html", etat=etat, seance=seance, lignes=lignes)


@app.route("/admin/cotisations/<int:id_cotisation>/annuler", methods=["POST"])
@role_requis(*GESTION)
def annuler_cotisation(id_cotisation):
    db = get_db()
    c = db.execute("SELECT * FROM cotisations WHERE id = ?", (id_cotisation,)).fetchone()
    if c is None:
        abort(404)
    db.execute("DELETE FROM cotisations WHERE id = ?", (id_cotisation,))
    recalculer_total(db, c["seance_id"])
    db.commit()
    flash("Cotisation annulée.", "info")
    return redirect(url_for("cotisations_seance", id_seance=c["seance_id"]))


@app.route("/admin/seances/<int:id_seance>/penaliser-retardataires", methods=["POST"])
@role_requis(*GESTION)
def penaliser_retardataires(id_seance):
    """Une pénalité de retard pour chaque membre qui n'a pas payé une séance passée."""
    db = get_db()
    seance = db.execute("SELECT * FROM seances WHERE id = ?", (id_seance,)).fetchone()
    if seance is None:
        abort(404)
    montant = entier(request.form.get("montant"), 100, 50000)
    if montant is None:
        flash("Montant de pénalité invalide (entre 100 et 50 000 FCFA).", "erreur")
    elif seance["date"] >= date.today().isoformat():
        flash("Cette séance n'est pas encore passée.", "erreur")
    else:
        cur = db.execute(
            "INSERT OR IGNORE INTO penalites (membre_id, seance_id, motif, montant) "
            "SELECT m.id, ?, 'retard', ? FROM membres m WHERE m.actif = 1 AND m.id NOT IN "
            "(SELECT membre_id FROM cotisations WHERE seance_id = ?)",
            (id_seance, montant, id_seance))
        db.commit()
        flash(f"{cur.rowcount} pénalité(s) de retard créée(s).",
              "succes" if cur.rowcount else "info")
    return redirect(url_for("cotisations_seance", id_seance=id_seance))


@app.route("/admin/penalites", methods=["GET", "POST"])
@role_requis(*CONSULTATION)
def admin_penalites():
    db, etat = charger_etat()
    if request.method == "POST":
        if not peut_gerer():
            abort(403)
        id_membre = entier(request.form.get("membre_id"))
        id_seance = entier(request.form.get("seance_id"))
        motif = request.form.get("motif", "")
        montant = entier(request.form.get("montant"), 100, 50000)
        erreurs = []
        if not id_membre or db.execute("SELECT 1 FROM membres WHERE id = ? AND actif = 1",
                                       (id_membre,)).fetchone() is None:
            erreurs.append("Membre inconnu.")
        if not id_seance or db.execute("SELECT 1 FROM seances WHERE id = ?",
                                       (id_seance,)).fetchone() is None:
            erreurs.append("Séance inconnue.")
        if motif not in MOTIFS:
            erreurs.append("Motif inconnu.")
        if montant is None:
            erreurs.append("Le montant doit être un entier entre 100 et 50 000 FCFA.")
        if erreurs:
            for e in erreurs:
                flash(e, "erreur")
        else:
            try:
                db.execute("INSERT INTO penalites (membre_id, seance_id, motif, montant) "
                           "VALUES (?, ?, ?, ?)", (id_membre, id_seance, motif, montant))
                db.commit()
                flash("Pénalité enregistrée.", "succes")
            except sqlite3.IntegrityError:
                flash("Ce membre a déjà une pénalité de ce motif pour cette séance.", "erreur")
        return redirect(url_for("admin_penalites"))
    return render_template("admin/penalites.html", etat=etat)


@app.route("/admin/penalites/<int:id_pen>/payer", methods=["POST"])
@role_requis(*GESTION)
def payer_penalite(id_pen):
    db = get_db()
    p = db.execute("SELECT * FROM penalites WHERE id = ?", (id_pen,)).fetchone()
    if p is None:
        abort(404)
    db.execute("UPDATE penalites SET payee = ? WHERE id = ?", (0 if p["payee"] else 1, id_pen))
    db.commit()
    flash("Pénalité marquée comme " + ("non payée." if p["payee"] else "payée."), "succes")
    return redirect(url_for("admin_penalites"))


@app.route("/admin/penalites/<int:id_pen>/supprimer", methods=["POST"])
@role_requis(*GESTION)
def supprimer_penalite(id_pen):
    db = get_db()
    db.execute("DELETE FROM penalites WHERE id = ?", (id_pen,))
    db.commit()
    flash("Pénalité supprimée.", "info")
    return redirect(url_for("admin_penalites"))

@app.route("/admin/membres", methods=["GET", "POST"])
@role_requis(*CONSULTATION)
def admin_membres():
    db, etat = charger_etat()
    if request.method == "POST":
        if not peut_gerer():
            abort(403)
        nom = " ".join(request.form.get("nom", "").split())
        tel = request.form.get("telephone", "").replace(" ", "")
        role = request.form.get("role", "membre")
        code = request.form.get("code", "")
        erreurs = []
        if len(nom) < 3:
            erreurs.append("Le nom doit contenir au moins 3 caractères.")
        if not RE_TEL.fullmatch(tel):
            erreurs.append("Téléphone invalide : 9 chiffres commençant par 6.")
        if role not in ROLES:
            erreurs.append("Rôle inconnu.")
        if len(code) < 6:
            erreurs.append("Le code d'accès doit contenir au moins 6 caractères.")
        if role in ("tresorier", "president") and db.execute(
                "SELECT 1 FROM membres WHERE role = ? AND actif = 1", (role,)).fetchone():
            erreurs.append(f"Il y a déjà un {ROLES[role].lower()} : un seul par tontine.")
        if not erreurs:
            ancien = db.execute("SELECT id, actif FROM membres WHERE telephone = ?",
                                (tel,)).fetchone()
            if ancien and ancien["actif"]:
                erreurs.append("Ce numéro de téléphone est déjà enregistré.")
            elif ancien:                      # ancien membre retiré : on le réactive
                db.execute("UPDATE membres SET actif = 1, nom = ?, empreinte = ?, role = ?, "
                           "date_adhesion = ? WHERE id = ?",
                           (nom, generate_password_hash(code), role,
                            date.today().isoformat(), ancien["id"]))
                db.commit()
                flash(f"{nom} est de retour dans la tontine.", "succes")
            else:
                db.execute(
                    "INSERT INTO membres (nom, telephone, date_adhesion, empreinte, role) "
                    "VALUES (?, ?, ?, ?, ?)",
                    (nom, tel, date.today().isoformat(), generate_password_hash(code), role))
                db.commit()
                flash(f"{nom} a rejoint la tontine.", "succes")
        for e in erreurs:
            flash(e, "erreur")
        return redirect(url_for("admin_membres"))
    return render_template("admin/membres.html", etat=etat)


@app.route("/admin/membres/<int:id_membre>/retirer", methods=["POST"])
@role_requis(*GESTION)
def retirer_membre(id_membre):
    """Retire un membre (actif = 0) : son historique de paiements est conservé."""
    db = get_db()
    membre = db.execute("SELECT * FROM membres WHERE id = ? AND actif = 1",
                        (id_membre,)).fetchone()
    if membre is None:
        abort(404)
    u = session["utilisateur"]
    if u["type"] == "membre" and u["id"] == id_membre:
        flash("Vous ne pouvez pas vous retirer vous-même.", "erreur")
    elif membre["role"] in ("tresorier", "president"):
        flash("Impossible de retirer le trésorier ou le président.", "erreur")
    else:
        
        db.execute("UPDATE seances SET beneficiaire_id = NULL "
                   "WHERE beneficiaire_id = ? AND date >= ?",
                   (id_membre, date.today().isoformat()))
        db.execute("UPDATE membres SET actif = 0 WHERE id = ?", (id_membre,))
        db.commit()
        flash(f"{membre['nom']} a été retiré de la tontine. Son historique est conservé.", "info")
    return redirect(url_for("admin_membres"))

@app.route("/admin/demandes")
@role_requis(*CONSULTATION)
def admin_demandes():
    db = get_db()
    en_attente = db.execute(
        "SELECT * FROM demandes_adhesion WHERE statut = 'en_attente' "
        "ORDER BY date_demande, id").fetchall()
    traitees = db.execute(
        "SELECT * FROM demandes_adhesion WHERE statut != 'en_attente' "
        "ORDER BY id DESC LIMIT 30").fetchall()
    return render_template("admin/demandes.html", en_attente=en_attente, traitees=traitees)


@app.route("/admin/demandes/<int:id_demande>/accepter", methods=["POST"])
@role_requis(*GESTION)
def accepter_demande(id_demande):
    """Accepte une demande : crée le compte du membre avec un code provisoire."""
    db = get_db()
    d = db.execute("SELECT * FROM demandes_adhesion WHERE id = ? AND statut = 'en_attente'",
                   (id_demande,)).fetchone()
    if d is None:
        abort(404)
    code = request.form.get("code", "")
    if len(code) < 6:
        flash("Le code d'accès provisoire doit contenir au moins 6 caractères.", "erreur")
        return redirect(url_for("admin_demandes"))

    aujourdhui = date.today().isoformat()
    existant = db.execute("SELECT id, actif FROM membres WHERE telephone = ?",
                          (d["telephone"],)).fetchone()
    if existant and existant["actif"]:
        db.execute("UPDATE demandes_adhesion SET statut = 'refusee' WHERE id = ?", (id_demande,))
        db.commit()
        flash("Ce numéro appartient déjà à un membre : la demande est classée comme refusée.",
              "erreur")
        return redirect(url_for("admin_demandes"))
    if existant:                                   # ancien membre retiré : on le réactive
        db.execute("UPDATE membres SET actif = 1, nom = ?, empreinte = ?, role = 'membre', "
                   "date_adhesion = ? WHERE id = ?",
                   (d["nom"], generate_password_hash(code), aujourdhui, existant["id"]))
    else:
        db.execute("INSERT INTO membres (nom, telephone, date_adhesion, empreinte, role) "
                   "VALUES (?, ?, ?, ?, 'membre')",
                   (d["nom"], d["telephone"], aujourdhui, generate_password_hash(code)))
    db.execute("UPDATE demandes_adhesion SET statut = 'acceptee' WHERE id = ?", (id_demande,))
    db.commit()
    flash(f"{d['nom']} est maintenant membre. Transmettez-lui son numéro "
          f"({d['telephone']}) et son code provisoire.", "succes")
    return redirect(url_for("admin_demandes"))


@app.route("/admin/demandes/<int:id_demande>/refuser", methods=["POST"])
@role_requis(*GESTION)
def refuser_demande(id_demande):
    db = get_db()
    cur = db.execute("UPDATE demandes_adhesion SET statut = 'refusee' "
                     "WHERE id = ? AND statut = 'en_attente'", (id_demande,))
    db.commit()
    if cur.rowcount == 0:
        abort(404)
    flash("Demande refusée.", "info")
    return redirect(url_for("admin_demandes"))


@app.route("/admin/historique")
@role_requis(*CONSULTATION)
def historique():
    _, etat = charger_etat()
    return render_template("admin/historique.html", etat=etat)

@app.route("/api/prochaine-seance")
def api_prochaine_seance():
    """Informations publiques sur la prochaine séance (page d'accueil)."""
    db = get_db()
    cycle = cycle_courant(db)
    if cycle is None:
        return sans_cache(jsonify(prochaine=None))
    etat = etat_cycle(db, cycle)
    p = etat["prochaine"]
    if p is None:
        return sans_cache(jsonify(prochaine=None, cycle=cycle["nom"]))
    return sans_cache(jsonify(
        prochaine=True, cycle=cycle["nom"], numero=p["numero"],
        total=len(etat["seances"]), date=p["date"], heure=HEURE_SEANCE,
        date_texte=filtre_date(p["date"], True), beneficiaire=p["beneficiaire_nom"],
        cagnotte=etat["attendu"], cotisation=etat["montant"],
        nb_membres=etat["nb_membres"]))

@app.route("/api/seances/<int:id_seance>/etat")
@api_role_requis("admin", "tresorier", "president", "membre")
def api_etat_seance(id_seance):
    """État d'une séance. Les noms des non-payeurs sont réservés à l'administration."""
    db = get_db()
    cycle = cycle_courant(db)
    if cycle is None:
        return jsonify(erreur="Aucun cycle."), 404
    etat = etat_cycle(db, cycle)
    s = next((x for x in etat["seances"] if x["id"] == id_seance), None)
    if s is None:
        return jsonify(erreur="Séance introuvable."), 404
    reponse = {
        "id": s["id"], "numero": s["numero"], "date": s["date"], "passee": s["passee"],
        "beneficiaire": s["beneficiaire_nom"], "cotisation": etat["montant"],
        "attendu": s["attendu"], "collecte": s["collecte"],
        "reste": s["attendu"] - s["collecte"],
        "nb_payes": s["nb_payes"], "nb_attendus": s["nb_attendus"],
        "nb_non_payes": s["nb_attendus"] - s["nb_payes"], "taux": s["taux"],
    }
    if session["utilisateur"]["role"] in CONSULTATION:
        payes = etat["par_seance"].get(id_seance, {})
        reponse["non_payes"] = [m["nom"] for m in etat["membres"] if m["id"] not in payes]
    return sans_cache(jsonify(reponse))

@app.route("/api/statistiques")
@api_role_requis(*CONSULTATION)
def api_statistiques():
    """Les 4 statistiques demandées, en JSON."""
    db = get_db()
    cycle = cycle_courant(db)
    if cycle is None:
        return jsonify(erreur="Aucun cycle."), 404
    etat = etat_cycle(db, cycle)
    return sans_cache(jsonify(
        cycle=etat["cycle"]["nom"], cotisation=etat["montant"], kpi=etat["kpi"],
        seances=[{"numero": s["numero"], "date": s["date"], "passee": s["passee"],
                  "beneficiaire": s["beneficiaire_nom"], "collecte": s["collecte"],
                  "attendu": s["attendu"], "taux": s["taux"]} for s in etat["seances"]],
        retardataires=[{"nom": i["nom"], "du": i["du"], "manquantes": i["manquantes"]}
                       for i in etat["retardataires"]],
        penalites=[{"nom": i["nom"], "total": i["pen_total"], "impayees": i["pen_impayees"]}
                   for i in sorted(etat["membres"], key=lambda i: -i["pen_total"])
                   if i["pen_total"] > 0],
        ponctualite=[{"nom": i["nom"], "taux": i["ponctualite"]}
                     for i in sorted(etat["membres"], key=lambda i: i["ponctualite"])]))

MESSAGES = {
    400: ("Requête refusée", "Votre session a expiré ou la requête est invalide. "
                             "Rechargez la page et recommencez."),
    403: ("Accès refusé", "Votre rôle ne permet pas d'accéder à cette page."),
    404: ("Page introuvable", "Cette adresse ne mène nulle part. Elle a peut-être été déplacée."),
    405: ("Méthode non autorisée", "Cette page ne s'utilise pas de cette façon."),
    500: ("Erreur du serveur", "Un problème est survenu de notre côté. Réessayez dans un instant."),
    503: ("Aucune donnée", "La base est vide. Lancez « python donnees_test.py » pour la remplir."),
}


def page_erreur(erreur):
    code = getattr(erreur, "code", 500)
    titre, message = MESSAGES.get(code, MESSAGES[500])
    return render_template("erreur.html", code=code, titre=titre, message=message), code


for _code in MESSAGES:
    app.register_error_handler(_code, page_erreur)


if __name__ == "__main__":
    app.run(debug=False)  