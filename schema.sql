PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS penalites;
DROP TABLE IF EXISTS cotisations;
DROP TABLE IF EXISTS seances;
DROP TABLE IF EXISTS cycles;
DROP TABLE IF EXISTS membres;
DROP TABLE IF EXISTS administrateurs;
DROP TABLE IF EXISTS demandes_adhesion;

CREATE TABLE administrateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    login TEXT NOT NULL UNIQUE,
    empreinte TEXT NOT NULL
);

CREATE TABLE membres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL CHECK (length(nom) >= 3),
    telephone TEXT NOT NULL UNIQUE
        CHECK (telephone GLOB '6[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    date_adhesion TEXT NOT NULL,
    empreinte TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'membre'
        CHECK (role IN ('membre', 'tresorier', 'president')),
    actif INTEGER NOT NULL DEFAULT 1 CHECK (actif IN (0, 1))
);

CREATE TABLE cycles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    montant_cotisation INTEGER NOT NULL CHECK (montant_cotisation > 0),
    periodicite TEXT NOT NULL CHECK (periodicite IN ('hebdomadaire', 'mensuelle')),
    date_debut TEXT NOT NULL
);

CREATE TABLE seances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cycle_id INTEGER NOT NULL REFERENCES cycles(id) ON DELETE CASCADE,
    numero INTEGER NOT NULL CHECK (numero >= 1),
    date TEXT NOT NULL,
    beneficiaire_id INTEGER REFERENCES membres(id),
    montant_total INTEGER NOT NULL DEFAULT 0 CHECK (montant_total >= 0),
    UNIQUE (cycle_id, numero),
    UNIQUE (cycle_id, beneficiaire_id)
);

CREATE TABLE cotisations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seance_id INTEGER NOT NULL REFERENCES seances(id) ON DELETE CASCADE,
    membre_id INTEGER NOT NULL REFERENCES membres(id),
    montant INTEGER NOT NULL CHECK (montant > 0),
    date_paiement TEXT NOT NULL,
    mode TEXT NOT NULL CHECK (mode IN ('especes', 'mobile_money')),
    UNIQUE (seance_id, membre_id)
);

CREATE TABLE penalites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    membre_id INTEGER NOT NULL REFERENCES membres(id),
    seance_id INTEGER NOT NULL REFERENCES seances(id) ON DELETE CASCADE,
    motif TEXT NOT NULL CHECK (motif IN ('retard', 'absence')),
    montant INTEGER NOT NULL CHECK (montant > 0),
    payee INTEGER NOT NULL DEFAULT 0 CHECK (payee IN (0, 1)),
    UNIQUE (membre_id, seance_id, motif)
);

CREATE TABLE demandes_adhesion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL CHECK (length(nom) >= 3),
    telephone TEXT NOT NULL
        CHECK (telephone GLOB '6[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]'),
    message TEXT,
    date_demande TEXT NOT NULL,
    statut TEXT NOT NULL DEFAULT 'en_attente'
        CHECK (statut IN ('en_attente', 'acceptee', 'refusee'))
);

CREATE UNIQUE INDEX idx_demande_attente ON demandes_adhesion (telephone)
    WHERE statut = 'en_attente';