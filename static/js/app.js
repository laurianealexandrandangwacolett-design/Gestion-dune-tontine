"use strict";

const formConnexion = document.querySelector("#form-connexion");
if (formConnexion) {
    const erreur = document.querySelector("#erreur");
    formConnexion.addEventListener("submit", (evenement) => {
        const messages = [];
        if (formConnexion.identifiant.value.trim() === "") {
            messages.push("Indiquez votre téléphone ou votre login.");
        }
        if (formConnexion.mot_de_passe.value === "") {
            messages.push("Indiquez votre mot de passe.");
        }
        if (messages.length > 0) {
            evenement.preventDefault();
            erreur.textContent = messages.join(" ");
        }
    });
}


document.querySelectorAll("form[data-confirmer]").forEach((formulaire) => {
    formulaire.addEventListener("submit", (evenement) => {
        if (!window.confirm(formulaire.dataset.confirmer)) {
            evenement.preventDefault();
        }
    });
});

document.querySelectorAll("[data-imprimer]").forEach((bouton) => {
    bouton.addEventListener("click", () => window.print());
});


document.querySelectorAll("input[data-filtre]").forEach((champ) => {
    const lignes = document.querySelectorAll(`${champ.dataset.filtre} tbody tr`);
    champ.addEventListener("input", () => {
        const recherche = champ.value.trim().toLowerCase();
        lignes.forEach((ligne) => {
            ligne.hidden = !ligne.textContent.toLowerCase().includes(recherche);
        });
    });
});


const formaterFcfa = (n) => Math.round(n).toLocaleString("fr-FR") + " FCFA";

async function chargerJson(url) {
    const reponse = await fetch(url, { headers: { Accept: "application/json" } });
    if (!reponse.ok) throw new Error("Erreur " + reponse.status);
    return reponse.json();
}

function afficherErreurs(formulaire, messages, evenement) {
    const zone = formulaire.querySelector(".erreur-form");
    if (messages.length > 0) {
        evenement.preventDefault();
        if (zone) zone.textContent = messages.join(" ");
    } else if (zone) {
        zone.textContent = "";
    }
}

const carteProchaine = document.querySelector("#prochaine-seance");
if (carteProchaine) {
    chargerProchaineSeance();
}

async function chargerProchaineSeance() {
    try {
        const d = await chargerJson("/api/prochaine-seance");
        if (!d.prochaine) {
            return;                                   
        }
        document.querySelector("#ps-numero").textContent = `Séance n° ${d.numero} sur ${d.total}`;
        document.querySelector("#ps-date").textContent = d.date_texte;
        document.querySelector("#ps-benef").textContent = d.beneficiaire || "à désigner";
        document.querySelector("#ps-cagnotte").textContent = formaterFcfa(d.cagnotte);
        demarrerCompteARebours(new Date(`${d.date}T${d.heure}:00`));
    } catch (e) {
        console.error("Impossible de charger la prochaine séance :", e);
    }
}

function demarrerCompteARebours(cible) {
    const jours = document.querySelector("#cr-j");
    const heures = document.querySelector("#cr-h");
    const minutes = document.querySelector("#cr-m");
    const secondes = document.querySelector("#cr-s");
    const deux = (n) => String(n).padStart(2, "0");
    let minuteur;

    function majCompteARebours() {
        const reste = Math.max(0, Math.floor((cible - Date.now()) / 1000));
        jours.textContent = deux(Math.floor(reste / 86400));
        heures.textContent = deux(Math.floor((reste % 86400) / 3600));
        minutes.textContent = deux(Math.floor((reste % 3600) / 60));
        secondes.textContent = deux(reste % 60);
        if (reste === 0) clearInterval(minuteur);     
    }
    majCompteARebours();
    minuteur = setInterval(majCompteARebours, 1000);
}

const grapheSeances = document.querySelector("#graph-seances");
const graphePonctualite = document.querySelector("#graph-ponctualite");
if (grapheSeances || graphePonctualite) {
    chargerStatistiques();
}

async function chargerStatistiques() {
    try {
        const stats = await chargerJson("/api/statistiques");
        if (grapheSeances) dessinerColonnes(grapheSeances, stats.seances);
        if (graphePonctualite) dessinerBarres(graphePonctualite, stats.ponctualite);
    } catch (e) {
        console.error("Impossible de charger les statistiques :", e);
    }
}

function dessinerColonnes(conteneur, seances) {
    conteneur.textContent = "";
    const grille = document.createElement("div");
    grille.className = "colonnes";
    for (const s of seances) {
        const colonne = document.createElement("div");
        colonne.className = "colonne" + (s.passee ? "" : " avenir");
        colonne.title = `Séance ${s.numero} : ${formaterFcfa(s.collecte)} sur ${formaterFcfa(s.attendu)}`;
        const pile = document.createElement("div");
        pile.className = "pile";
        const rempli = document.createElement("div");
        rempli.className = "rempli";
        rempli.style.height = s.taux + "%";
        const numero = document.createElement("span");
        numero.className = "num";
        numero.textContent = s.numero;                
        pile.appendChild(rempli);
        colonne.append(pile, numero);
        grille.appendChild(colonne);
    }
    const legende = document.createElement("p");
    legende.className = "petit";
    legende.textContent = "Hauteur = part du montant attendu collecté. Vert : séances passées. Doré : séances à venir (paiements d'avance).";
    conteneur.append(grille, legende);
}

function dessinerBarres(conteneur, lignes) {
    conteneur.textContent = "";
    const liste = document.createElement("div");
    liste.className = "barres-h";
    for (const l of lignes) {
        const ligne = document.createElement("div");
        ligne.className = "ligne-h";
        const nom = document.createElement("span");
        nom.textContent = l.nom;
        const piste = document.createElement("div");
        piste.className = "piste";
        const valeur = document.createElement("div");
        valeur.className = "valeur-h " + (l.taux >= 85 ? "bon" : l.taux >= 60 ? "moyen" : "faible");
        valeur.style.width = l.taux + "%";
        piste.appendChild(valeur);
        const pourcentage = document.createElement("span");
        pourcentage.textContent = l.taux + " %";
        ligne.append(nom, piste, pourcentage);
        liste.appendChild(ligne);
    }
    conteneur.appendChild(liste);
}

const resumeSeance = document.querySelector("#resume-seance");
if (resumeSeance) {
    initialiserResume(resumeSeance);
}

async function initialiserResume(resume) {
    try {
        const etat = await chargerJson(`/api/seances/${resume.dataset.seance}/etat`);
        const formulaire = document.querySelector("#form-cotisations");
        const cases = formulaire ? [...formulaire.querySelectorAll('input[name="membre"]')] : [];

        function afficher() {
            const nouveaux = cases.filter((c) => c.checked).length;
            const collecte = etat.collecte + nouveaux * etat.cotisation;
            const taux = etat.attendu ? Math.min(100, Math.round((100 * collecte) / etat.attendu)) : 0;
            document.querySelector("#r-collecte").textContent = formaterFcfa(collecte);
            document.querySelector("#r-reste").textContent = formaterFcfa(Math.max(0, etat.attendu - collecte));
            document.querySelector("#r-non").textContent = etat.nb_non_payes - nouveaux;
            document.querySelector("#r-barre").style.width = taux + "%";
        }

        cases.forEach((c) => c.addEventListener("change", afficher));
        const toutCocher = document.querySelector("#tout-cocher");
        if (toutCocher) {
            toutCocher.addEventListener("click", () => {
                const tousCoches = cases.every((c) => c.checked);
                cases.forEach((c) => { c.checked = !tousCoches; });
                afficher();
            });
        }
        afficher();
    } catch (e) {
        console.error("Impossible de charger l'état de la séance :", e);
    }
}

const formPenalite = document.querySelector("#form-penalite");
if (formPenalite) {
    formPenalite.addEventListener("submit", (evenement) => {
        const champs = formPenalite.elements;
        const montant = Number(champs.montant.value);
        const messages = [];
        if (champs.membre_id.value === "") messages.push("Choisissez un membre.");
        if (!Number.isInteger(montant) || montant < 100 || montant > 50000) {
            messages.push("Le montant doit être un entier entre 100 et 50 000 FCFA.");
        }
        afficherErreurs(formPenalite, messages, evenement);
    });
}

const formMembre = document.querySelector("#form-membre");
if (formMembre) {
    formMembre.addEventListener("submit", (evenement) => {
        const champs = formMembre.elements;
        const messages = [];
        if (champs.nom.value.trim().length < 3) {
            messages.push("Le nom doit contenir au moins 3 caractères.");
        }
        if (!/^6\d{8}$/.test(champs.telephone.value.replace(/\s/g, ""))) {
            messages.push("Téléphone invalide : 9 chiffres commençant par 6.");
        }
        if (champs.code.value.length < 6) {
            messages.push("Le code d'accès doit contenir au moins 6 caractères.");
        }
        afficherErreurs(formMembre, messages, evenement);
    });
}

const boutonMenu = document.querySelector("#bouton-menu");
const menuPrincipal = document.querySelector("#menu-principal");
if (boutonMenu && menuPrincipal) {
    const basculerMenu = (ouvrir) => {
        menuPrincipal.classList.toggle("ouvert", ouvrir);
        boutonMenu.setAttribute("aria-expanded", String(ouvrir));
        boutonMenu.setAttribute("aria-label", ouvrir ? "Fermer le menu" : "Ouvrir le menu");
    };
    boutonMenu.addEventListener("click", () => {
        basculerMenu(!menuPrincipal.classList.contains("ouvert"));
    });
    document.addEventListener("keydown", (evenement) => {
        if (evenement.key === "Escape") basculerMenu(false);  
    });
}

document.querySelectorAll(".flash.succes, .flash.info").forEach((message) => {
    setTimeout(() => message.classList.add("efface"), 7000);
});

const boutonVoirMdp = document.querySelector("#voir-mdp");
if (boutonVoirMdp) {
    boutonVoirMdp.addEventListener("click", () => {
        const champ = document.querySelector("#mot_de_passe");
        const visible = champ.type === "text";
        champ.type = visible ? "password" : "text";
        boutonVoirMdp.textContent = visible ? "Afficher" : "Masquer";
        boutonVoirMdp.setAttribute("aria-label",
            visible ? "Afficher le mot de passe" : "Masquer le mot de passe");
    });
}

const formAdhesion = document.querySelector("#form-adhesion");
if (formAdhesion) {
    const champMessage = formAdhesion.elements.message;
    const compteur = document.querySelector("#compteur-message");

    const majCompteur = () => {
        compteur.textContent = `${champMessage.value.length} / 300`;
    };
    champMessage.addEventListener("input", majCompteur);
    majCompteur();

    formAdhesion.addEventListener("submit", (evenement) => {
        const champs = formAdhesion.elements;
        const messages = [];
        const nom = champs.nom.value.trim();
        if (nom.length < 3 || nom.length > 80) {
            messages.push("Le nom doit contenir entre 3 et 80 caractères.");
        }
        if (!/^6\d{8}$/.test(champs.telephone.value.replace(/\s/g, ""))) {
            messages.push("Téléphone invalide : 9 chiffres commençant par 6.");
        }
        if (champMessage.value.length > 300) {
            messages.push("Le message ne doit pas dépasser 300 caractères.");
        }
        afficherErreurs(formAdhesion, messages, evenement);
    });
}