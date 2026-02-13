import mysql.connector
import bcrypt
from dotenv import load_dotenv
import os

load_dotenv()
# ========================== CONNEXION DB ==========================
connection = mysql.connector.connect(
    host= os.getenv("DB_HOST"),
    user=  os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    database= os.getenv("DB_NAME")
)

if connection.is_connected():
    print("✅ Connexion à la base de données réussie!")

# ========================== GESTION MOT DE PASSE ==========================
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

# ========================== INSCRIPTION ==========================
def inscription():
    cursor = connection.cursor()
    
    while True:
        nom = input("Votre nom : ")
        prenom = input("Votre prénom : ")
        if nom.isalpha() and prenom.isalpha():
            break
        print(" Nom et prénom doivent contenir uniquement des lettres.")

    while True:
        email = input("Votre email : ")
        if '@' in email and ' ' not in email:
            break
        print(" Email invalide.")

    while True:
        password = input("Votre mot de passe : ")
        if len(password) >= 6:  # minimum 6 caractères
            password_hashed = hash_password(password)
            break
        print(" Le mot de passe doit contenir au moins 6 caractères.")

    while True:
        role = input("Rôle (apprenant/admin) : ").lower()
        if role in ["apprenant", "admin"]:
            break
        print(" Rôle invalide.")

    try:
        query = """
        INSERT INTO users(nom_user, prenom_user, mail_user, password, role_user)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nom, prenom, email, password_hashed, role))
        connection.commit()
        print(" Inscription réussie !")
    except Exception as e:
        print(f" Erreur lors de l'inscription : {e}")
    finally:
        cursor.close()

# ========================== CONNEXION ==========================
def connexion():
    cursor = connection.cursor(dictionary=True)
    email = input("Votre email : ")
    password = input("Votre mot de passe : ")

    query = "SELECT * FROM users WHERE mail_user = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        print(" Aucun compte associé à cet email.")
        return None

    if not verify_password(password, user['password']):
        print(" Mot de passe incorrect.")
        return None

    print(f" Bienvenue {user['prenom_user']} ({user['role_user']})")
    return user['id_user'], user['role_user'] 


# ========================== MENU APPRENANT ==========================
# ========================== CREER UN TICKET ==========================
def creer_ticket(id_user):
    cursor = connection.cursor()
    titre = input("Titre du ticket : ")
    description = input("Description du problème : ")
    niveau_urgence = input("Urgence (faible/moyen/critique) : ")
    status = input(" status") 

    query = """
    INSERT INTO demandes
    (titre_demande, description_demande, niveau_urgence, status_demande, id_user)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (titre, description, niveau_urgence, status, id_user))
    connection.commit()
    cursor.close()
    print("Ticket créé avec succès !")

def voir_historique(id_user):
    cursor = connection.cursor(dictionary=True)
    
    query = """
    SELECT titre_demande, description_demande, niveau_urgence, status_demande
    FROM demandes
    WHERE id_user = %s
    ORDER BY id_demande DESC
    """
    cursor.execute(query, (id_user,))
    tickets = cursor.fetchall()
    cursor.close()

    if not tickets:
        print("Aucun ticket enregistré.")
        return

    print("\n VOTRE HISTORIQUE DE TICKETS :")
    for t in tickets:
        print(f"- {t['titre_demande']} | {t['niveau_urgence']} | {t['status_demande']}")

def menu_apprenant(id_user):
    while True:
        print("\n--- MENU APPRENANT ---")
        print("1. Créer un ticket")
        print("2. Voir mon historique")
        print("3. Déconnexion")
        try:
            choix = int(input("Choix (1-3) : "))
        except ValueError:
            print(" Choix invalide")
            continue

        match choix:
            case 1:
                creer_ticket(id_user)
            case 2:
                voir_historique(id_user)
            case 3:
                main()
                break
            case _:
                print(" Choix incorrect")

# ========================== MENU Admin==========================
def menu_admin(id_user):
    while True:
        print("\n--- MENU ADMIN ---")
        print("1. Listes apprenants")
        print("2. Voir historique")
        print("3. Listes des demandes plus urgent")
        print("4. Reponses demandes")
        print("5. Déconnexion")
        try:
            choix = int(input("Choix (1-5) : "))
            # if 1 <= choix <= 4:
        except ValueError:
            print(" Choix invalide")
            continue

        match choix:
            case 1:
                liste_apprenants(id_user)
                print("liste apprenant")
            case 2:
                historiques(id_user)
            case 3:
                liste_plus_urgents(id_user)
            case 4:
                reponses(id_user)
            case 5:
                main()
                break
            case _:
                print(" Choix incorrect")

def liste_apprenants(id_user):
    cursor = connection.cursor(dictionary=True)
    query ="""
            select nom_user,prenom_user,mail_user
            from users
            """
    cursor.execute(query)
    resultat = cursor.fetchall()
    cursor.close()


    if not resultat:
        print("Aucun apprenant!")

        return
    
    print("\n ---Listes des apprenants ----")
    for apprenant in resultat:
        print(f"- {apprenant['nom_user']} | {apprenant['prenom_user']} | {apprenant['mail_user']}")

def historiques(id_user):
    cursor = connection.cursor(dictionary=True)

    query = """
            select us.nom_user,us.prenom_user,us.mail_user,
            de.titre_demande,de.description_demande, de.niveau_urgence, de.status_demande
            from users us 
            join demandes de on de.id_user = us.id_user
           """
    cursor.execute(query)
    resultat = cursor.fetchall()
    cursor.close()

    if not resultat:
        print("Historique vide")
        return
    print(f"\n --- Historiques ---")
    for histo in resultat:
        print(f"\n Apprenants: {histo['nom_user']} | {histo['prenom_user']} | {histo['mail_user']}")
        print(f"\n Demandes: {histo['titre_demande']} | {histo['description_demande']} | {histo['niveau_urgence']} | {histo['status_demande']}")

def liste_plus_urgents(id_user):
    cursor = connection.cursor(dictionary=True)

    query = """
            select us.nom_user,us.prenom_user,us.mail_user,
            de.titre_demande,de.description_demande, de.niveau_urgence, de.status_demande
            from users us 
            join demandes de on de.id_user = us.id_user where de.niveau_urgence = 'critique'
           """
    cursor.execute(query)
    resultat = cursor.fetchall()
    cursor.close()
    if not resultat:
        print("Historique vide")
        return
    print(f"\n --- Historiques ---")
    for histo in resultat:
        print(f"- Apprenants {histo['nom_user']}| {histo['prenom_user']} | {histo['mail_user']}")
        print(f"- Demandes {histo['titre_demande']}| {histo['description_demande']} | {histo['niveau_urgence']} | {histo['status_demande']}")

def reponses(id_user):
    cursor = connection.cursor(dictionary=True)
    query = """
            select us.id_user, us.nom_user,us.prenom_user,us.mail_user,
            de.id_demande,de.titre_demande,de.description_demande, de.niveau_urgence, de.status_demande
            from users us 
            join demandes de on de.id_user = us.id_user
            
        """
    cursor.execute(query)
    resultat = cursor.fetchall()
    # cursor.close()

    if not resultat:
        print("Historique vide")
        return
    print(f"\n --- Historiques des demandes correspondant a un aprrenant---")
    for histo in resultat:
        print(f"\n Apprenants: {histo['id_user']} | {histo['nom_user']} | {histo['prenom_user']} | {histo['mail_user']}")
        print(f"\n Demandes: {histo['id_demande']} | {histo['titre_demande']} | {histo['description_demande']} | {histo['niveau_urgence']} | {histo['status_demande']}")
        continue

    id_demande = int(input("L'id du demande d'un apprenant "))
    repondre = (input("Reponse (en-attente\en-cours\ resolu) "))
    query2 = """
            update demandes
            set status_demande = %s
            where id_demande = %s
            """   
    
    cursor.execute(query2, (repondre,id_demande))

    connection.commit()
    cursor.close()
    return historiques(id_user)

# ========================== MENU PRINCIPAL ==========================
def main():
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. S'inscrire")
        print("2. Se connecter")
        print("3. Quitter")

        try:
            choix = int(input("Choix (1-3) : "))
        except ValueError:
            print(" Choix invalide")
            continue

        match choix:
            case 1:
                inscription()
            case 2:
                result = connexion()
                if result:
                    id_user, role = result
                    print(f" result {result}")
                    if role == "apprenant":
                        menu_apprenant(id_user)
                    elif role == "admin":
                        menu_admin(id_user)
                    else:
                        print("oups erreur!")
            case 3:
                print("Au revoir !")
                break
            case _:
                print(" Choix incorrect")

# ========================== LANCEMENT ==========================
if __name__ == "__main__":
    main()
