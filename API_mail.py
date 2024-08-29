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




locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
paris_tz = timezone(timedelta(hours=2))



def reply_to_unread_messages(gmail_service, context, info):
    print("Lecture des messages non-lus en cours...")
    messages = get_messages(gmail_service)

    num_messages = len(messages)
    if num_messages == 1:
        print("1 mail non-lu.")
    elif num_messages > 1:
        print(f"{num_messages} mails non-lus.")
    else:
        print("Aucun message non-lu.")
        return

    
    for message in messages:
        raw_email = get_message_body(message["raw"])

        print("Génération de la réponse en cours...")
        reply = make_reply(raw_email, context)

        current_date = datetime.now(paris_tz).strftime("%a, %d %b %Y %H:%M:%S %z")
        sender_name = message["json"]["sender_name"]
        sender_email = message["json"]["sender_email"]
        subject = message["json"]["subject"]
        message_id = message["json"]["message_id"]

        reply_block = "\n".join(["> " + line for line in raw_email.split("\n")])
        raw_reply = reply + f"\n\nLe {current_date}, {sender_name} <{sender_email}> a écrit:\n\n" + reply_block

        my_info = info["name"] + " <"+info["email"]+">"
        re_subject = "Re: " + subject.removeprefix("Re: ")

        headers = {
            "In-Reply-To": message_id,
            "References": message_id,
        }

        new_message = create_message(my_info, sender_email, re_subject, raw_reply, headers)

        print("Création du brouillon en cours...")
        create_draft(gmail_service, new_message)

        print("Message marqué comme lu.")
        mark_message_as_read(gmail_service, message["json"]["id"])

        print("Fini !")

    if num_messages == 1:
        print("Brouillon créé pour 1 message.")
    else:
        print(f"Brouillons créés pour {num_messages} messages.")




SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
]




client = OpenAI(api_key='clé_API')



def get_services():
    creds = None
    if os.path.exists('token.pickle'):
        os.remove('token.pickle')

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return {
        "gmail": build('gmail', 'v1', credentials=creds),
        "people": build('people', 'v1', credentials=creds),
    }




def get_user_info(service):
    profile = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()
    name = profile['names'][0]['displayName']
    email = profile['emailAddresses'][0]['value']
    return {"name": name, "email": email}



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



def send_message(service, message):
    message = service.users().messages().send(userId='me', body=message).execute()
    print(f"Message envoyé: {message['id']}")
    return message



def get_message_body(message):
    msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    msg_str = email.message_from_bytes(msg_raw)

    if msg_str.is_multipart():
        for part in msg_str.walk():
            if part.get_content_type() == 'text/plain':
                body = part.get_payload(decode=True).decode()
                return body
    else:
        body = msg_str.get_payload(decode=True).decode()
        return body



def mark_message_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print(f"Message ID {msg_id} marqué comme lu.")




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





def create_draft(service, message):
    draft = service.users().drafts().create(userId='me', body={'message': message}).execute()
    print(f"Brouillon créé avec l'ID : {draft['id']}")
    return draft



def reply_to_unread_messages(gmail_service, context, info):
    print("Lecture des messages non-lus en cours...")
    messages = get_messages(gmail_service)

    num_messages = len(messages)
    if num_messages == 1:
        print("1 mail non-lu.")
    elif num_messages > 1:
        print(f"{num_messages} mails non-lus.")
    else:
        print("Aucun message non-lu.")
        return

    for message in messages:
        raw_email = get_message_body(message["raw"])

        print("Génération de la réponse en cours...")
        reply = make_reply(raw_email, context)

        current_date = datetime.now(paris_tz).strftime("%a, %d %b %Y %H:%M:%S %z")
        sender_name = message["json"]["sender_name"]
        sender_email = message["json"]["sender_email"]
        subject = message["json"]["subject"]
        message_id = message["json"]["message_id"]

        reply_block = "\n".join(["> " + line for line in raw_email.split("\n")])
        raw_reply = reply + f"\n\nLe {current_date}, {sender_name} <{sender_email}> a écrit:\n\n" + reply_block

        my_info = info["name"] + " <"+info["email"]+">"
        re_subject = "Re: " + subject.removeprefix("Re: ")

        headers = {
            "In-Reply-To": message_id,
            "References": message_id,
        }

        new_message = create_message(my_info, sender_email, re_subject, raw_reply, headers)

        print("Création du brouillon en cours...")
        create_draft(gmail_service, new_message) 

        print("Message marqué comme lu.")
        mark_message_as_read(gmail_service, message["json"]["id"])

        print("Fini !")

    if num_messages == 1:
        print("Brouillon créé pour 1 message.")
    else:
        print(f"Brouillons créés pour {num_messages} messages.")




def main():
    if len(sys.argv) == 2:
        with open(sys.argv[1], "r") as f:
            context = f.read()
    else:
        context = ""

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

    if input() != "oui":
        print("Fermeture du programme.")
        sys.exit()

    print("Authentification...")
    services = get_services() 

    gmail_service = services["gmail"]
    people_service = services["people"]

    print("Authentification réussie !")
    info = get_user_info(people_service)

    while True:
        reply_to_unread_messages(gmail_service, context, info)
        print("Attente (10 secondes)...")
        time.sleep(10)




if __name__ == '__main__':
    main()
