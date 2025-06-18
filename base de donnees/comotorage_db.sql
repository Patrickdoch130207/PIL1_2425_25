CREATE DATABASE comotorage_db;
USE comotorage_db;
CREATE TABLE utilisateur (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100),
    prenom VARCHAR(100),
    email VARCHAR(254) UNIQUE,
    password VARCHAR(255) NOT NULL DEFAULT 'temporary_password',
    telephone VARCHAR(15),
    ville VARCHAR(100),
    pays VARCHAR(100),
    sexe VARCHAR(10),
    photo_profil VARCHAR(100) DEFAULT 'photos_profil/profile_defaut.png',
    role VARCHAR(20),
    profil_complet BOOLEAN DEFAULT FALSE
);

CREATE TABLE passwordresetcode (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    code VARCHAR(6),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES utilisateur(id) ON DELETE CASCADE
);

CREATE TABLE trajet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    conducteur_id INT,
    point_depart VARCHAR(100),
    destination VARCHAR(100),
    date_depart DATE,
    heure_depart TIME,
    depart_longitude FLOAT,
    depart_latitude FLOAT,
    dest_longitude FLOAT,
    dest_latitude FLOAT,
    sieges_dispo INT,
    prix INT,
    type_vehicule VARCHAR(50),
    marque_vehicule VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    preferences JSON,
    FOREIGN KEY (conducteur_id) REFERENCES utilisateur(id)
);

CREATE TABLE trajet_passagers (
    trajet_id INT,
    utilisateur_id INT,
    PRIMARY KEY (trajet_id, utilisateur_id),
    FOREIGN KEY (trajet_id) REFERENCES trajet(id),
    FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id)
);

CREATE TABLE demandetrajet (
    id INT AUTO_INCREMENT PRIMARY KEY,
    passager_id INT,
    point_depart VARCHAR(255),
    destination VARCHAR(255),
    date_depart DATE,
    heure_depart TIME,
    depart_longitude FLOAT,
    depart_latitude FLOAT,
    dest_longitude FLOAT,
    dest_latitude FLOAT,
    statut VARCHAR(20) DEFAULT 'en_attente',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    preferences JSON,
    FOREIGN KEY (passager_id) REFERENCES utilisateur(id)
);

CREATE TABLE reservation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    trajet_id INT,
    passager_id INT,
    statut VARCHAR(20) DEFAULT 'en_attente',
    date_reservation DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (trajet_id) REFERENCES trajet(id),
    FOREIGN KEY (passager_id) REFERENCES utilisateur(id)
);

CREATE TABLE message (
    id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT,
    receiver_id INT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES utilisateur(id),
    FOREIGN KEY (receiver_id) REFERENCES utilisateur(id)
);
