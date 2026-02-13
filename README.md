Application de gestion de tickets (Python + MySQL)
Description

Cette application en Python (mode console) permet la gestion des utilisateurs et des tickets de support.
Elle implémente un système d’inscription et de connexion sécurisé, avec une gestion des rôles utilisateur (apprenant / administrateur) et le suivi des demandes.

Technologies utilisées

Python 3

MySQL

mysql-connector-python

bcrypt

python-dotenv

Sécurité

Les mots de passe sont chiffrés avec bcrypt

Les informations sensibles de connexion à la base de données sont stockées dans un fichier .env

Exemple de fichier .env :

DB_HOST=localhost
DB_USER=your_user
DB_PASSWORD=your_password
DB_NAME=your_database

Fonctionnalités
Utilisateur (Apprenant)

Inscription avec validation des champs

Connexion sécurisée

Création de tickets

Consultation de l’historique personnel

Administrateur

Consultation de la liste des apprenants

Affichage de l’historique global des tickets

Filtrage des tickets urgents

Mise à jour du statut des demandes

Structure de la base de données (résumé)
Table users

id_user

nom_user

prenom_user

mail_user

password

role_user

Table demandes

id_demande

titre_demande

description_demande

niveau_urgence

status_demande

id_user (clé étrangère)

Lancement de l’application
python main.py

Objectif pédagogique

Ce projet permet de mettre en pratique :

la connexion Python–MySQL

la gestion des rôles utilisateurs

le hashage sécurisé des mots de passe

la structuration logique d’une application backend
