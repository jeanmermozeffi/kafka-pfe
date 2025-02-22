-- create_tables.sql

-- Créer la table Vehicule si elle n'existe pas
CREATE TABLE IF NOT EXISTS Vehicule (
    id SERIAL PRIMARY KEY,
    Immatriculation VARCHAR(255),
    Marque VARCHAR(255),
    Modele VARCHAR(255),
    Annee INT,
    Vehicule VARCHAR(255),
    Prix NUMERIC,
    DatePublication DATE
);

-- Créer la table 'Resumer' si elle n'existe pas
CREATE TABLE IF NOT EXISTS Resumer (
    id SERIAL PRIMARY KEY, -- Colonne d'identifiant unique pour chaque enregistrement
    energie VARCHAR(255),
    puissance_commerciale VARCHAR(255),
    puissance_fiscale VARCHAR(255),
    consommation_mixte VARCHAR(255),
    emission_de_co2 VARCHAR(255),
    boite_de_vitesses VARCHAR(255),
    carrosserie VARCHAR(255),
    date_de_fin_de_commercialisation VARCHAR(255),
    immatriculation UUID UNIQUE NOT NULL -- Clé unique pour l'immatriculation
);

-- Créer la table Dimensions si elle n'existe pas
CREATE TABLE IF NOT EXISTS Dimensions (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    longueur VARCHAR(255),
    largeur VARCHAR(255),
    hauteur VARCHAR(255),
    empattement VARCHAR(255),
    reservoir VARCHAR(255),
    porte_a_faux_avant VARCHAR(255),
    porte_a_faux_arriere VARCHAR(255),
    voies_avant VARCHAR(255),
    voies_arriere VARCHAR(255),
    garde_au_sol VARCHAR(255),
    angle_dattaque VARCHAR(255),
    angle_ventral VARCHAR(255),
    angle_de_fuite VARCHAR(255),
    Immatriculation VARCHAR(255)
);

-- Créer la table Weight si elle n'existe pas
CREATE TABLE IF NOT EXISTS Weight (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    poids_a_vide VARCHAR(255),
    ptac VARCHAR(255),
    ptra VARCHAR(255),
    charge_utile VARCHAR(255),
    poids_tracte_freine VARCHAR(255),
    poids_tracte_non_freine VARCHAR(255),
    Immatriculation VARCHAR(255)
);

-- Créer la table Habitability si elle n'existe pas
CREATE TABLE IF NOT EXISTS Habitability (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    nombre_de_places INT,
    volume_de_coffre VARCHAR(255),
    volume_de_coffre_utile VARCHAR(255),
    hauteur_de_seuil_de_chargement VARCHAR(255),
    longueur_utile VARCHAR(255),
    largeur_utile VARCHAR(255),
    Immatriculation VARCHAR(255)
);

-- Créer la table Tires si elle n'existe pas
CREATE TABLE IF NOT EXISTS Tires (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    types_de_pneumatiques VARCHAR(255),
    materiau_des_jantes VARCHAR(255),
    taille_des_roues_avant VARCHAR(255),
    taille_des_roues_arriere VARCHAR(255),
    type_de_roues_de_secours VARCHAR(255),
    Immatriculation VARCHAR(255)
);

-- Créer la table Engine si elle n'existe pas
CREATE TABLE IF NOT EXISTS Engine (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    Nom_du_moteur VARCHAR(255),
    Energie VARCHAR(255),
    Architecture VARCHAR(255),
    Alimentation VARCHAR(255),
    Injection VARCHAR(255),
    Cylindree VARCHAR(255),
    Puissance_reelle_maxi VARCHAR(255),
    Au_regime_de VARCHAR(255),
    Couple_maxi VARCHAR(255),
    Nombre_de_soupapes INT,
    Alesage_course VARCHAR(255),
    Rapport_volumetrique VARCHAR(255),
    Norme_anti_pollution VARCHAR(255),
    Disposition_du_moteur VARCHAR(255)
);

-- Créer la table Transmission si elle n'existe pas
CREATE TABLE IF NOT EXISTS Transmission (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    Boite_de_vitesses VARCHAR(255),
    Mode_de_transmission VARCHAR(255)
);

-- Créer la table Technical si elle n'existe pas
CREATE TABLE IF NOT EXISTS Technical (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    Type_de_chassis VARCHAR(255),
    Materiau_du_chassis VARCHAR(255),
    Direction_assistee VARCHAR(3),  -- Oui/Non
    Type_de_direction VARCHAR(255),
    Type_dassistance VARCHAR(255),
    Diametre_de_braquage_trottoir VARCHAR(255),
    Type_de_suspension_avant VARCHAR(255),
    Type_de_suspension_arriere VARCHAR(255)
);

-- Créer la table Performance si elle n'existe pas
CREATE TABLE IF NOT EXISTS Performance (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    Vitesse_maximale VARCHAR(255),
    acceleration_0_100_kmh VARCHAR(255),  -- 0 à 100 km/h
    Immatriculation VARCHAR(255)
);

-- Créer la table Consumption si elle n'existe pas
CREATE TABLE IF NOT EXISTS Consumption (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    Mixte VARCHAR(255),
    Emission_de_CO2 VARCHAR(255),
    Immatriculation VARCHAR(255)
);

-- Créer la table GalleryImages si elle n'existe pas
CREATE TABLE IF NOT EXISTS GalleryImages (
    id SERIAL PRIMARY KEY,
    vehicule_id INT REFERENCES Vehicule(id),
    image_url TEXT,
    Immatriculation VARCHAR(255)
);