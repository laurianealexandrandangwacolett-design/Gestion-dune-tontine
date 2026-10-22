# Projet 9 : Gestion d'une tontine (Groupe 09)

Application Web de gestion d'une tontine (épargne tournante) : suivi des cotisations, des séances, des bénéficiaires, des retards et des pénalités, avec un espace pour chaque membre et un espace d'administration pour le trésorier.

- **Matière** : Technologies Web et applications (évaluation finale)
- **Enseignant** : M FOTSO T. Valdez W.
- **Filière et niveau** : GLO, niveau 5
- **Technologies** : HTML5, CSS3, JavaScript, Python 3, Flask, SQLite


# Sommaire

1. [Présentation](#présentation)
2. [Fonctionnalités](#fonctionnalités)
3. [Prérequis](#prérequis)
4. [Installation](#installation)
5. [Lancement](#lancement)
6. [Comptes de test](#comptes-de-test)
7. [Recréer les données de test](#recréer-les-données-de-test)
8. [Exporter et restaurer la base](#exporter-et-restaurer-la-base)
9. [Structure du projet](#structure-du-projet)
10. [Base de données](#base-de-données)
11. [Routes](#routes)
12. [API JSON](#api-json)
13. [Règles de gestion et formules](#règles-de-gestion-et-formules)
14. [Sécurité](#sécurité)
15. [Tests et validation](#tests-et-validation)
16. [Dépannage](#dépannage)
17. [Limites et améliorations possibles](#limites-et-améliorations-possibles)
18. [Équipe](#équipe)

---

## Présentation

Dans une tontine, chaque membre cotise le **même montant** à chaque séance, et **à tour de rôle** un membre reçoit toute la cagnotte. Avec les données de test : 25 membres, 10 000 FCFA par séance, donc une cagnotte de 250 000 FCFA à chaque séance, et 25 séances (une par membre).

Le trésorier tenait tout dans un cahier, ce qui causait des erreurs de calcul, des retards oubliés et des disputes. Ce site rend la gestion **transparente** : tout est enregistré dans une base de données, et les retards, montants dus, taux de ponctualité et statistiques sont **recalculés automatiquement** à partir des paiements enregistrés. Aucun chiffre n'est saisi à la main.

---

## Fonctionnalités

### Visiteur (sans connexion)

- Page d'accueil avec la prochaine séance, son bénéficiaire, la cagnotte attendue et un **compte à rebours**.
- **Calendrier** des 25 séances avec le bénéficiaire de chacune et l'avancement des cotisations (sans montants individuels).
- **Demande d'adhésion** : formulaire public (nom, téléphone, message) pour demander à rejoindre la tontine au prochain cycle.

### Membre

- Connexion avec son numéro de téléphone et son code d'accès.
- **Mon espace** : cotisations payées, montant dû, pénalités, taux de ponctualité, date et montant de son bénéfice.
- Une ligne par séance : « payée à l'heure », « payée en retard », « non payée » ou « à venir ».
- **Changement du code d'accès** (ancien code, nouveau code, confirmation).

### Trésorier (droits de gestion)

- **Enregistrement des cotisations** d'une séance sur une seule page, avec totaux mis à jour en direct, choix du mode (espèces ou mobile money) et annulation d'un paiement.
- **Désignation du bénéficiaire** de chaque séance, avec **tirage au sort** des bénéficiaires manquants.
- **Pénalités** : ajout, marquage « payée », suppression, et pénalité de retard appliquée en un clic à tous les retardataires d'une séance.
- **Membres** : ajout d'un membre avec un code d'accès provisoire, retrait d'un membre (l'historique est conservé).
- **Demandes d'adhésion** : liste des demandes en attente (avec compteur), acceptation (création du compte avec un code provisoire) ou refus.
- **Historique imprimable** du cycle pour l'assemblée générale.

### Président (consultation seulement)

- Accède à toutes les pages d'administration, mais **ne peut rien modifier** (les boutons sont masqués et le serveur refuse les envois avec une erreur 403).

### Administrateur (compte de test)

- Compte réservé à l'enseignant pour tester l'espace d'administration, avec les mêmes droits que le trésorier.

### Tableau de bord et statistiques

1. **Montant collecté par séance**, comparé au montant attendu (graphique et tableau).
2. **Membres en retard** et montant dû par chacun.
3. **Total des pénalités par membre** (dont les impayées).
4. **Taux de ponctualité de chaque membre**.

---

## Prérequis

- **Python 3.10 ou plus récent** (testé avec Python 3.12).
- **pip** (installé avec Python).
- Un navigateur récent (Chrome, Edge, Firefox).
- Aucun serveur de base de données à installer : SQLite est intégré à Python.

Vérifier la version de Python :

```
python --version
```

---

## Installation

Ouvrir un terminal **dans le dossier `projet`** (celui qui contient `app.py`).

### Windows (PowerShell)

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Si PowerShell refuse d'activer l'environnement (erreur sur les scripts), lancer une fois :

```
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

puis recommencer `venv\Scripts\activate`.

### Linux ou macOS

```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Le terminal doit afficher `(venv)` au début de la ligne quand l'environnement est actif.

---

## Lancement

La base **`projet.db` est déjà remplie** : il n'y a rien d'autre à préparer.

```
python app.py
```

Puis ouvrir dans le navigateur : **http://127.0.0.1:5000**

Pour arrêter le serveur : **Ctrl+C** dans le terminal.

> Le serveur est lancé avec `debug=False` (version rendue). Il ne se recharge donc pas tout seul : après toute modification d'un fichier Python, l'arrêter (Ctrl+C) puis le relancer.

---

## Comptes de test

Le **login** d'un membre est son **numéro de téléphone** (9 chiffres, sans espaces).

| Rôle | Identifiant | Mot de passe | Droits |
|---|---|---|---|
| Administrateur | `admin` | `Admin!2026` | Gestion complète (compte pour l'enseignant) |
| Trésorier (Mbarga Jean-Pierre) | `677000001` | `Tresor!2026` | Gestion complète |
| Président (Ngo Bassa Colette) | `677000002` | `Pres!2026` | Consultation seulement |
| Membres (23 comptes) | `677000003` à `677000025` | `Membre!2026` | Espace personnel |

Exemples de parcours à tester :

1. **Visiteur** : accueil, calendrier, puis `/rejoindre` pour envoyer une demande d'adhésion.
2. **Membre** (`677000003` / `Membre!2026`) : « Mon espace ». L'adresse `/admin` donne une page **403 Accès refusé**.
3. **Trésorier** (`677000001` / `Tresor!2026`) : Administration, Séances, ouvrir la séance 13, cocher des membres et enregistrer. Puis l'onglet **Demandes** pour accepter ou refuser une demande.
4. **Président** (`677000002` / `Pres!2026`) : mêmes pages en lecture seule.

---

## Recréer les données de test

Le script `donnees_test.py` crée la base `projet.db` à partir de `schema.sql` et la remplit avec des données réalistes. **Attention : il supprime la base existante** (paiements, membres ajoutés et demandes d'adhésion compris).

```
python donnees_test.py
```

Résultat attendu (environ) :

| Table | Lignes |
|---|---|
| `administrateurs` | 1 |
| `membres` | 25 |
| `cycles` | 1 |
| `seances` | 25 |
| `cotisations` | 280 |
| `penalites` | 37 |
| `demandes_adhesion` | 0 |

Contenu des données de test :

- 25 membres, dont un trésorier et un président.
- Un cycle hebdomadaire de 25 séances, cotisation de 10 000 FCFA.
- **12 séances déjà passées**, la 13e est la prochaine (le samedi à venir, calculée à partir de la date du jour).
- 22 bénéficiaires déjà désignés ; les 3 dernières séances n'en ont pas (pour tester la désignation et le tirage au sort).
- Des cotisations ponctuelles, en retard ou manquantes ; 9 membres ont payé d'avance la prochaine séance.
- Des pénalités de retard et d'absence, payées ou non.

Le générateur utilise `random.seed(42)` : les données sont **les mêmes à chaque lancement** (à la date près).

---

## Exporter et restaurer la base

Le fichier `export_projet.sql` contient toute la base en SQL lisible (structure et données). Il permet de recréer la base même si `projet.db` est abîmé.

**Exporter** (depuis le dossier `projet`) :

```
python -c "import sqlite3; db=sqlite3.connect('projet.db'); open('export_projet.sql','w',encoding='utf-8').write('\n'.join(db.iterdump()))"
```

**Restaurer** (supprimer d'abord `projet.db`, puis) :

```
python -c "import sqlite3; sqlite3.connect('projet.db').executescript(open('export_projet.sql', encoding='utf-8').read())"
```

---

## Structure du projet

```
projet/
├── app.py                  Application Flask : routes, calculs, sécurité
├── schema.sql              Création des tables et des contraintes
├── donnees_test.py         Remplit la base de données de test
├── projet.db               Base SQLite déjà remplie
├── export_projet.sql       Export complet de la base
├── requirements.txt        Dépendances Python
├── README.md               Ce fichier
├── static/
│   ├── css/style.css       Feuille de style (mobile d'abord, 2 points de rupture)
│   ├── js/app.js           JavaScript : vérifications, fetch, graphiques
│   └── images/             logo.svg, motif.svg
└── templates/              Gabarits Jinja2 (héritent de base.html)
    ├── base.html           En-tête, menu, messages, pied de page
    ├── macros.html         Avatar des membres
    ├── index.html          Accueil
    ├── calendrier.html     Calendrier public
    ├── connexion.html      Connexion
    ├── rejoindre.html      Demande d'adhésion
    ├── mon_espace.html     Espace du membre
    ├── erreur.html         Pages d'erreur (400, 403, 404, 405, 500, 503)
    └── admin/
        ├── _nav.html           Onglets de l'administration
        ├── tableau_bord.html   Statistiques et graphiques
        ├── seances.html        Séances et bénéficiaires
        ├── cotisations.html    Cotisations d'une séance
        ├── penalites.html      Pénalités
        ├── membres.html        Membres
        ├── demandes.html       Demandes d'adhésion
        └── historique.html     Historique imprimable
```

---

## Base de données

SQLite, **7 tables** liées par des clés étrangères (activées avec `PRAGMA foreign_keys = ON`).

| Table | Rôle | Colonnes principales |
|---|---|---|
| `administrateurs` | Comptes d'administration | `login` (unique), `empreinte` du mot de passe |
| `membres` | Membres de la tontine | `nom`, `telephone` (unique), `date_adhesion`, `empreinte`, `role`, `actif` |
| `cycles` | Un cycle de la tontine | `nom`, `montant_cotisation`, `periodicite`, `date_debut` |
| `seances` | Les séances d'un cycle | `cycle_id`, `numero`, `date`, `beneficiaire_id`, `montant_total` |
| `cotisations` | Paiements des membres | `seance_id`, `membre_id`, `montant`, `date_paiement`, `mode` |
| `penalites` | Pénalités | `membre_id`, `seance_id`, `motif`, `montant`, `payee` |
| `demandes_adhesion` | Demandes faites par les visiteurs | `nom`, `telephone`, `message`, `date_demande`, `statut` |

### Relations

- un **cycle** a plusieurs **séances** ;
- une **séance** a un bénéficiaire (un **membre**) et plusieurs **cotisations** ;
- un **membre** a plusieurs **cotisations** et plusieurs **pénalités** ;
- une **pénalité** concerne un membre et une séance.

### Contraintes importantes

| Contrainte | Effet |
|---|---|
| `UNIQUE (cycle_id, beneficiaire_id)` | Un membre ne bénéficie **qu'une seule fois** par cycle |
| `UNIQUE (seance_id, membre_id)` | Une seule cotisation par membre et par séance |
| `UNIQUE (membre_id, seance_id, motif)` | Pas de pénalité en double |
| `CHECK` sur `telephone` | 9 chiffres commençant par 6 |
| `CHECK` sur `role`, `mode`, `motif`, `statut`, `periodicite` | Seules les valeurs prévues sont acceptées |
| `CHECK` sur les montants | Montants strictement positifs, 1 à 20 personnes, etc. |
| `NOT NULL` sur les champs essentiels | Pas de donnée incomplète |
| Index unique partiel sur `demandes_adhesion` | Une seule demande **en attente** par numéro |
| `ON DELETE CASCADE` sur `seances` | La suppression d'un cycle supprime ses séances |

Ces règles sont appliquées **par la base elle-même** : même un bug dans le code Python ne peut pas enregistrer de doublon.


## Routes

**Droits** : *Consultation* = trésorier, président, administrateur. *Gestion* = trésorier, administrateur.

### Pages publiques et espace membre

| Adresse | Méthode | Accès | Rôle |
|---|---|---|---|
| `/` | GET | Public | Accueil |
| `/calendrier` | GET | Public | Calendrier des séances |
| `/rejoindre` | GET, POST | Public | Demande d'adhésion |
| `/connexion` | GET, POST | Public | Connexion |
| `/deconnexion` | POST | Connecté | Déconnexion |
| `/mon-espace` | GET | Membre | Espace personnel |
| `/mon-espace/code` | POST | Membre | Changer son code d'accès |

### Administration

| Adresse | Méthode | Accès | Rôle |
|---|---|---|---|
| `/admin` | GET | Consultation | Tableau de bord |
| `/admin/seances` | GET | Consultation | Séances et bénéficiaires |
| `/admin/seances/<id>/beneficiaire` | POST | Gestion | Désigner le bénéficiaire |
| `/admin/cycles/<id>/tirage` | POST | Gestion | Tirage au sort des bénéficiaires manquants |
| `/admin/seances/<id>/cotisations` | GET, POST | Consultation / Gestion | Enregistrer les cotisations |
| `/admin/cotisations/<id>/annuler` | POST | Gestion | Annuler une cotisation |
| `/admin/seances/<id>/penaliser-retardataires` | POST | Gestion | Pénalité de retard pour tous les retardataires |
| `/admin/penalites` | GET, POST | Consultation / Gestion | Liste et ajout de pénalités |
| `/admin/penalites/<id>/payer` | POST | Gestion | Marquer payée ou non payée |
| `/admin/penalites/<id>/supprimer` | POST | Gestion | Supprimer une pénalité |
| `/admin/membres` | GET, POST | Consultation / Gestion | Liste et ajout de membres |
| `/admin/membres/<id>/retirer` | POST | Gestion | Retirer un membre (désactivation) |
| `/admin/demandes` | GET | Consultation | Demandes d'adhésion |
| `/admin/demandes/<id>/accepter` | POST | Gestion | Accepter une demande |
| `/admin/demandes/<id>/refuser` | POST | Gestion | Refuser une demande |
| `/admin/historique` | GET | Consultation | Historique imprimable |

Les **pages d'erreur** (400, 403, 404, 405, 500, 503) sont personnalisées et héritent du même gabarit.

---

## API JSON

Trois routes renvoient du JSON (`jsonify`). Elles sont utilisées par le JavaScript avec `fetch`.

| Route | Accès | Contenu |
|---|---|---|
| `GET /api/prochaine-seance` | Public | Prochaine séance, bénéficiaire, cagnotte, heure (compte à rebours) |
| `GET /api/seances/<id>/etat` | Connecté | Montants et nombre de payeurs d'une séance (les noms des non-payeurs sont réservés à l'administration) |
| `GET /api/statistiques` | Consultation | Les 4 statistiques du tableau de bord |

Sans connexion, les routes protégées répondent en JSON `401` (connexion requise) ou `403` (accès refusé), et **pas** par une page HTML.

Exemple de réponse de `/api/prochaine-seance` (les valeurs dépendent de la date du jour) :

```json
{
  "prochaine": true,
  "cycle": "Cycle 2026-2027",
  "numero": 13,
  "total": 25,
  "date": "2026-10-17",
  "heure": "16:00",
  "date_texte": "samedi 17 oct. 2026",
  "beneficiaire": "Nom du bénéficiaire",
  "cagnotte": 250000,
  "cotisation": 10000,
  "nb_membres": 25
}
```

Structure de `/api/statistiques` : `kpi` (chiffres clés), `seances` (collecté et attendu par séance), `retardataires` (nom, montant dû, séances manquées), `penalites` (total et impayées par membre), `ponctualite` (taux par membre).



## Règles de gestion et formules

| Notion | Règle |
|---|---|
| Séance passée | Sa date est antérieure à aujourd'hui |
| Cagnotte attendue | Nombre de membres actifs × montant de la cotisation (ex. 25 × 10 000 = 250 000 FCFA) |
| Séances dues par un membre | Séances passées **depuis son adhésion** (un nouveau membre ne doit pas les séances d'avant son arrivée) |
| Montant dû | Séances dues non payées × montant de la cotisation |
| Cotisation ponctuelle | Payée au plus tard le jour de la séance |
| Taux de ponctualité | Cotisations ponctuelles ÷ séances dues (une cotisation manquante compte comme non ponctuelle) |
| Taux de recouvrement | Collecté sur les séances passées ÷ attendu sur les séances passées |
| Bénéficiaire | Un membre actif, une seule fois par cycle |
| Montant d'une cotisation | Toujours égal à la cotisation du cycle (le trésorier ne saisit pas de montant) |

Toutes ces valeurs sont calculées par la fonction `etat_cycle` de `app.py` à chaque affichage, à partir des tables `seances`, `cotisations` et `penalites`.

**Retrait d'un membre** : il n'est pas supprimé, il est **désactivé** (`actif = 0`). Son historique de paiements est conservé, il ne compte plus dans la cagnotte attendue, il perd ses tours à venir et ne peut plus se connecter. Un numéro retiré peut être réactivé en le rajoutant.


## Sécurité

| Protection | Mise en œuvre |
|---|---|
| **Mots de passe hachés** | `generate_password_hash` / `check_password_hash` (Werkzeug) : la base ne contient que des empreintes |
| **Requêtes SQL paramétrées** | Toutes les requêtes utilisent des `?` : pas d'injection SQL |
| **Protection CSRF** | Un jeton secret par session est exigé sur **tous** les envois POST (erreur 400 sinon) |
| **Rôles vérifiés côté serveur** | Décorateurs `connexion_requise` et `role_requis` : accès refusé (403) même si l'adresse est tapée à la main |
| **Échappement du HTML** | Jinja2 échappe les valeurs ; le JavaScript utilise `textContent` : un nom contenant `<script>` s'affiche comme du texte |
| **Données revérifiées par le serveur** | Dates, montants, téléphones, rôles et modes de paiement sont contrôlés même si le JavaScript est contourné |
| **Modifications en POST uniquement** | Aucune suppression ni modification par un simple lien |
| **Session** | Nouvelle session à la connexion, cookie signé avec `SECRET_KEY` |
| **Redirections sûres** | Seules les adresses internes sont acceptées après connexion |
| **En-têtes HTTP** | `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` |
| **Demande d'adhésion publique** | Vérifiée côté serveur, limitée à 50 demandes en attente, message identique pour un numéro déjà membre (ne révèle pas qui est membre) |
| **Mode debug** | `debug=False` dans la version rendue |

> **Avant une vraie mise en ligne** : définir une `SECRET_KEY` longue et secrète (variable d'environnement) à la place de la valeur de développement, utiliser un serveur de production (Gunicorn ou Waitress) et sauvegarder régulièrement `projet.db`.



## Tests et validation

Vérifications réalisées pendant le développement :

- **30 tests automatiques de sécurité**, tous réussis : accès refusé sans connexion, accès par rôle (membre, président, trésorier), envois sans jeton CSRF refusés, injection SQL à la connexion refusée, redirection vers un site extérieur bloquée, demandes d'adhésion invalides refusées, mots de passe hachés, mode debug désactivé.
- **Test d'injection de code (XSS)** : un nom de membre égal à `<script>alert("XSS")</script>` s'affiche comme du texte, sans exécution.
- **Parcours manuels** de chaque fonctionnalité, avec des saisies correctes et fausses.
- **Validateur W3C** (https://validator.w3.org) sur les pages principales.
- **Test sur trois largeurs** (téléphone, tablette, ordinateur) avec les outils de développement du navigateur.

Les captures d'écran et les résultats détaillés figurent dans le rapport PowerPoint.



## Dépannage

| Problème | Solution |
|---|---|
| `No module named 'flask'` | L'environnement virtuel n'est pas activé : refaire `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Linux, macOS), puis `pip install -r requirements.txt` |
| `no such table` ou erreur sur la base | Lancer `python donnees_test.py` pour recréer la base |
| Le navigateur affiche un autre site sur le port 5000 | Un ancien serveur occupe le port : le fermer, ou le terminer avec `Get-Process python -ErrorAction SilentlyContinue \| Stop-Process -Force` (Windows PowerShell), puis relancer `python app.py` |
| Erreur 400 « Requête refusée » | La session a expiré : recharger la page (Ctrl+F5) et recommencer |
| `ERR_CONNECTION_REFUSED` | Le serveur n'est pas lancé : exécuter `python app.py` |
| Les modifications du code n'apparaissent pas | Le mode debug est désactivé : arrêter (Ctrl+C) et relancer `python app.py`, puis Ctrl+F5 dans le navigateur |
| Un code d'accès ne fonctionne plus | Il a été changé : recréer les comptes avec `python donnees_test.py` |


## Limites et améliorations possibles

**Limites actuelles**

- Pas de paiement en ligne : le trésorier enregistre l'argent reçu (espèces ou mobile money) à la main.
- Pas de réinitialisation automatique d'un code d'accès oublié.
- Un seul cycle est géré à la fois (le plus récent).
- Un membre qui arrive en cours de cycle n'a pas de tour de bénéficiaire : l'inscription est prévue pour le **cycle suivant**.
- Pas d'envoi de notifications (SMS ou e-mail).

**Améliorations envisagées**

- Notifications SMS avant chaque séance et en cas de retard.
- Intégration d'un service de paiement Mobile Money.
- Création et gestion de plusieurs cycles depuis le site.
- Réinitialisation du code d'accès par le trésorier.
- Export PDF de l'historique et envoi d'un reçu au membre.
- Envoi d'une photo ou d'une preuve de paiement.



**Groupe 09**, Projet 9 : Gestion d'une tontine (GLO, niveau 5).

Projet réalisé par:  MBETMI NDANGWA COLETTE LAURIANNE

