import os
import sys
import time
import pickle
import base64
import email
import locale
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from openai import OpenAI
from tqdm import tqdm
import pyfiglet
from colorama import init, Fore, Style

# Initialiser colorama
init(autoreset=True)

# Configuration locale et timezone
locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
paris_tz = timezone(timedelta(hours=2))

# Scopes nécessaires
SCOPES = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.modify',
]

## put your API key here



def print_stylized_intro():
    # Générer un titre stylé avec pyfiglet
    title = pyfiglet.figlet_format("IAcine   Mail", font="standard")
    print(Fore.CYAN + title)

    # Message d'avertissement stylé avec couleurs
    disclaimers = (
        Fore.GREEN + "Your Gmail Assistant that manages your messages.\n \n" +
        Fore.YELLOW + "This program retrieves and analyzes the content of your unread emails\n" +
        "using a local LLM, ensuring security and confidentiality.\n \n" +
        Fore.MAGENTA + "Type 'yes' to continue.\n \n" +
        Fore.RED + "© 2025 IAcine. All rights reserved.\n \n"
    )
    print(disclaimers)


def get_services():
    creds = None
    # Vérification de l'existence d'un token déjà existant
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si pas de credentials valides, on lance le flow d'authentification
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Rafraîchit le jeton expiré sans repasser par le navigateur
            creds.refresh(Request())
        else:
            # Pas de token ou pas de refresh_token -> Authentification via navigateur
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Sauvegarde du nouveau jeton
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return {
        "gmail": build('gmail', 'v1', credentials=creds),
        "people": build('people', 'v1', credentials=creds),
    }


def get_user_info(service):
    profile = service.people().get(resourceName='people/me', personFields='names,emailAddresses').execute()
    name = profile['names'][0]['displayName']
    email_address = profile['emailAddresses'][0]['value']
    return {"name": name, "email": email_address}


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
    print(Fore.GREEN + f"Message sent: {message['id']}")
    return message


def get_message_body(message):
    msg_raw = base64.urlsafe_b64decode(message['raw'].encode('ASCII'))
    msg_str = email.message_from_bytes(msg_raw)

    if msg_str.is_multipart():
        for part in msg_str.walk():
            if part.get_content_type() == 'text/plain':
                return part.get_payload(decode=True).decode()
    else:
        return msg_str.get_payload(decode=True).decode()


def mark_message_as_read(service, msg_id):
    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={'removeLabelIds': ['UNREAD']}
    ).execute()
    print(Fore.BLUE + f"Message ID {msg_id} marked as read.")


def get_messages(service):
    results = service.users().messages().list(userId='me', labelIds=['UNREAD']).execute()
    messages = results.get('messages', [])
    message_list = []

    for message in messages:
        msg_raw = service.users().messages().get(userId='me', id=message['id'], format="raw").execute()
        msg_json = service.users().messages().get(userId='me', id=message['id']).execute()

        headers = msg_json["payload"]["headers"]
        sender_name, sender_email = None, None

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
    prompt = f"Respond professionally and appropriately to this email:\n\n{raw_email}\n\nAdditional context: {context}"

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an intelligent assistant who responds to incoming emails."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()


def create_draft(service, message):
    draft = service.users().drafts().create(userId='me', body={'message': message}).execute()
    print(Fore.CYAN + f"Draft created with ID : {draft['id']}")
    return draft


def reply_to_unread_messages(gmail_service, context, info):
    print(Fore.YELLOW + "Reading unread messages...")
    messages = get_messages(gmail_service)

    num_messages = len(messages)
    if num_messages == 1:
        print(Fore.GREEN + "1 unread email.")
    elif num_messages > 1:
        print(Fore.GREEN + f"{num_messages} unread emails.")
    else:
        print(Fore.RED + "No unread messages.")
        return

    for message in messages:
        raw_email = get_message_body(message["raw"])
        print(Fore.YELLOW + "Generating reply...")
        reply = make_reply(raw_email, context)

        current_date = datetime.now(paris_tz).strftime("%a, %d %b %Y %H:%M:%S %z")
        sender_name = message["json"]["sender_name"]
        sender_email = message["json"]["sender_email"]
        subject = message["json"]["subject"]
        message_id = message["json"]["message_id"]

        reply_block = "\n".join(["> " + line for line in raw_email.split("\n")])
        raw_reply = reply + f"\n\nLe {current_date}, {sender_name} <{sender_email}> a écrit:\n\n" + reply_block

        my_info = f'{info["name"]} <{info["email"]}>'
        re_subject = "Re: " + subject.removeprefix("Re: ")

        headers = {
            "In-Reply-To": message_id,
            "References": message_id,
        }

        new_message = create_message(my_info, sender_email, re_subject, raw_reply, headers)

        print(Fore.YELLOW + "Creating draft...")
        create_draft(gmail_service, new_message)

        print(Fore.BLUE + "Marked as read.")
        mark_message_as_read(gmail_service, message["json"]["id"])

        print(Fore.GREEN + "Finished!")

    if num_messages == 1:
        print(Fore.GREEN + "Draft created for 1 message.")
    else:
        print(Fore.GREEN + f"Drafts created for {num_messages} messages.")


def main():
    print_stylized_intro()
    user_input = input().strip().lower()
    if user_input != "yes":
        print(Fore.RED + "Exiting the program.")
        sys.exit()

    print(Fore.YELLOW + "Authenticating...")
    services = get_services()
    gmail_service = services["gmail"]
    people_service = services["people"]
    print(Fore.GREEN + "Authentication successful!")

    info = get_user_info(people_service)

    while True:
        reply_to_unread_messages(gmail_service, context="", info=info)
        print(Fore.MAGENTA + "Waiting (60 sec)...")

        # Affiche une barre de chargement de 10 secondes
        for _ in tqdm(range(60), desc="Waiting", bar_format="{l_bar}{bar} {remaining}"):
            time.sleep(1)


if __name__ == '__main__':
    main()
