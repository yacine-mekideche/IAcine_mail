# Importation des bibliothèques nécessaires
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import pickle
import base64
import email
import time
import sys
import os
from openai import OpenAI
import locale
from datetime import datetime, timedelta, timezone



# Configuration de la locale pour le français et le fuseau horaire de Paris
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
paris_tz = timezone(timedelta(hours=2))



# Fonction principale pour traiter les emails non-lus
def reply_to_unread_messages(gmail_service, context, info):
    print("Lecture des messages non-lus en cours...")
    messages = get_messages(gmail_service)  # Récupère les messages non-lus

    num_messages = len(messages)  # Compte le nombre de messages non-lus
    if num_messages == 1:
        print("1 mail non-lu.")
    elif num_messages > 1:
        print(f"{num_messages} mails non-lus.")
    else:
        print("Aucun message non-lu.")
        return

    # Boucle à travers chaque message non-lu
    for message in messages:
        raw_email = get_message_body(message["raw"])  # Récupère le corps du message

        print("Génération de la réponse en cours...")
        reply = make_reply(raw_email, context)  # Génère une réponse via GPT-3.5

        # Formatage de la date et heure actuelle en français
        current_date = datetime.now(paris_tz).strftime("%a, %d %b %Y %H:%M:%S %z")
        sender_name = message["json"]["sender_name"]
        sender_email = message["json"]["sender_email"]
        subject = message["json"]["subject"]
        message_id = message["json"]["message_id"]

        # Construction du bloc de réponse avec l'email original en citation
        reply_block = "\n".join(["> " + line for line in raw_email.split("\n")])
        raw_reply = reply + f"\n\nLe {current_date}, {sender_name} <{sender_email}> a écrit:\n\n" + reply_block

        # Informations sur l'expéditeur et sujet de la réponse
        my_info = info["name"] + " <"+info["email"]+">"
        re_subject = "Re: " + subject.removeprefix("Re: ")

        # Préparation des en-têtes de l'email
        headers = {
            "In-Reply-To": message_id,
            "References": message_id,
        }

        # Création du message pour le brouillon
        new_message = create_message(my_info, sender_email, re_subject, raw_reply, headers)

        print("Création du brouillon en cours...")
        create_draft(gmail_service, new_message)  # Stocke le message en tant que brouillon

        print("Message marqué comme lu.")
        mark_message_as_read(gmail_service, message["json"]["id"])  # Marque le message comme lu

        print("Fini !")

    # Affichage du nombre de brouillons créés
    if num_messages == 1:
        print("Brouillon créé pour 1 message.")
    else:
        print(f"Brouillons créés pour {num_messages} messages.")




# Liste des autorisations demandées pour accéder à Gmail et d'autres services Google
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
]



# Initialisation du client OpenAI avec la clé API
client = OpenAI(api_key='clé_API')  # Remplacez par votre clé API




# Fonction pour initialiser les services Google nécessaires (Gmail, People)
def get_services():
    creds = None
    # Suppression du fichier de token précédent pour forcer une nouvelle authentification
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')

    # Chargement des identifiants d'accès s'ils existent
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si les identifiants ne sont pas valides ou manquants, demander l'authentification
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Retourne les services Gmail et People avec les credentials obtenus
    return {
        "gmail": build('gmail', 'v1', credentials=creds),
        "people": build('people', 'v1', credentials=creds),
    }




# Fonction pour obtenir les informations de l'utilisateur connecté (nom, email)
def get_user_info(service):
    profile = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()
    name = profile['names'][0]['displayName']
    email = profile['emailAddresses'][0]['value']
    return {"name": name, "email": email}




# Fonction pour créer un message email
def create_message(sender, to, subject, message_text, headers=None):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    if headers:
        for name, value in headers.items():
            message[name] = value
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}




# Fonction pour envoyer un message email via l'API Gmail
def send_message(service, message):
    message = service.users().messages().send(userId='me', body=message).execute()
    print(f"Message envoyé: {message['id']}")
    return message




# Fonction pour récupérer le corps d'un message email
def get_message_body(message):
    msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    msg_str = email.message_from_bytes(msg_raw)

    # Si le message est multipart, on prend la partie text/plain
    if msg_str.is_multipart():
        for part in msg_str.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode()
                return body
    else:
        body = msg_str.get_payload(decode=True).decode()
        return body




# Fonction pour marquer un message comme lu
def mark_message_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print(f"Message ID {msg_id} marqué comme lu.")




# Fonction pour récupérer les messages non-lus
def get_messages(service):
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    messages = results.get('messages', [])

    message_list = []

    for message in messages:
        msg_raw = service.users().messages().get(userId='me', id=message['id'], format="raw").execute()
        msg_json = service.users().messages().get(userId='me', id=message['id']).execute()

        headers = msg_json["payload"]["headers"]
        for header in headers:
            if header["name"] == "From":
                sender = header["value"]
                if "<" in sender and ">" in sender:
                    sender_name = sender.split("<")[0].strip()
                    sender_email = sender.split("<")[1].strip().removesuffix(">")
                else:
                    sender_name = sender
                    sender_email = sender
                msg_json["sender_name"] = sender_name
                msg_json["sender_email"] = sender_email
            if header["name"] == "Subject":
                msg_json["subject"] = header["value"]
            if header["name"] == "Message-ID":
                msg_json["message_id"] = header["value"]

        message_list.append({
            "raw": msg_raw,
            "json": msg_json,
        })

    return message_list




# Fonction pour générer une réponse à l'aide du modèle GPT-3.5
def make_reply(raw_email, context):
    prompt = f"Répondez de manière professionnelle et appropriée à cet email:\n\n{raw_email}\n\nContexte supplémentaire: {context}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un assistant intelligent qui répond aux emails reçus."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()





# Fonction pour créer un brouillon d'email
def create_draft(service, message):
    draft = service.users().drafts().create(userId='me', body={'message': message}).execute()
    print(f"Brouillon créé avec l'ID : {draft['id']}")
    return draft




# Fonction principale pour lire les emails non-lus et générer des brouillons de réponses
def reply_to_unread_messages(gmail_service, context, info):
    print("Lecture des messages non-lus en cours...")
    messages = get_messages(gmail_service)  # Récupère les messages non-lus

    num_messages = len(messages)  # Compte le nombre de messages non-lus
    if num_messages == 1:
        print("1 mail non-lu.")  # Affiche qu'il y a 1 email non-lu
    elif num_messages > 1:
        print(f"{num_messages} mails non-lus.")  # Affiche le nombre d'emails non-lus
    else:
        print("Aucun message non-lu.")  # Si aucun message n'est non-lu, quitte la fonction
        return

    # Boucle à travers chaque message non-lu pour générer une réponse et la sauvegarder en brouillon
    for message in messages:
        raw_email = get_message_body(message["raw"])  # Récupère le corps du message

        print("Génération de la réponse en cours...")
        reply = make_reply(raw_email, context)  # Génère une réponse via GPT-3.5

        # Formatage de la date et heure actuelle en français
        current_date = datetime.now(paris_tz).strftime("%a, %d %b %Y %H:%M:%S %z")
        sender_name = message["json"]["sender_name"]
        sender_email = message["json"]["sender_email"]
        subject = message["json"]["subject"]
        message_id = message["json"]["message_id"]

        # Construction du bloc de réponse avec l'email original en citation
        reply_block = "\n".join(["> " + line for line in raw_email.split("\n")])
        raw_reply = reply + f"\n\nLe {current_date}, {sender_name} <{sender_email}> a écrit:\n\n" + reply_block

        # Informations sur l'expéditeur et sujet de la réponse
        my_info = info["name"] + " <"+info["email"]+">"
        re_subject = "Re: " + subject.removeprefix("Re: ")

        # Préparation des en-têtes de l'email
        headers = {
            "In-Reply-To": message_id,
            "References": message_id,
        }

        # Création du message pour le brouillon
        new_message = create_message(my_info, sender_email, re_subject, raw_reply, headers)

        print("Création du brouillon en cours...")
        create_draft(gmail_service, new_message)  # Stocke le message en tant que brouillon

        print("Message marqué comme lu.")
        mark_message_as_read(gmail_service, message["json"]["id"])  # Marque le message comme lu

        print("Fini !")

    # Affichage du nombre de brouillons créés
    if num_messages == 1:
        print("Brouillon créé pour 1 message.")
    else:
        print(f"Brouillons créés pour {num_messages} messages.")




# Fonction principale du programme
def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            context = f.read()  # Lit le contexte depuis un fichier si fourni en argument
    else:
        context = ""

    # Affiche le message de bienvenue et les instructions pour continuer
    print( "##########################################" )
    print( "##                                      ##" )
    print( "##        Bienvenue sur IAcine !        ##" )
    print( "##                                      ##" )
    print( "##        Votre IAssistant Gmail        ##" )
    print( "##         qui gère vos messages.       ##" )
    print( "##                                      ##" )
    print( "##########################################" )
    print( "##                                      ##" )
    print( "##              ATTENTION :             ##" )
    print( "##   Ce programme récupère et traite    ##" )
    print( "##      le contenu de vos e-mails       ##" )
    print( "##         non-lus via GPT-3.5.         ##" )
    print( "##                                      ##" )
    print( "##      Tapez 'oui' pour continuer      ##" )
    print( "##                                      ##" )
    print( "##########################################" )
    print( "##       © 2024 - Yacine Mekideche.     ##" )
    print( "##         Tous droits réservés.        ##" )
    print( "##########################################" )

    # Si l'utilisateur ne tape pas "oui", le programme se ferme
    if input() != "oui":
        print("Fermeture du programme.")
        sys.exit()

    print("Authentification...")
    services = get_services()  # Authentifie l'utilisateur et obtient les services nécessaires

    gmail_service = services["gmail"]
    people_service = services["people"]

    print("Authentification réussie !")
    info = get_user_info(people_service)  # Récupère les informations de l'utilisateur

    # Boucle infinie pour vérifier les emails toutes les 10 secondes
    while True:
        reply_to_unread_messages(gmail_service, context, info)  # Répond aux emails non-lus
        print("Attente (10 secondes)...")
        time.sleep(10)




# Point d'entrée du programme
if __name__ == '__main__':
    main()
