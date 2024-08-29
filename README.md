# IAcine_mail : Votre IA-ssistant Gmail à portée de main !

![image](https://github.com/user-attachments/assets/8329e85e-9169-4bd5-9ae2-f99335ca1b1e)

## Introduction

La gestion quotidienne des emails peut rapidement devenir une tâche fastidieuse, transformant notre boîte de réception en un espace saturé et désorganisé. Beaucoup d'entre nous rêvent d'une boîte de réception vide à la fin de la journée, mais cela semble souvent hors de portée.

C'est de cette frustration qu'est née l'idée de créer IAcine_mail : un assistant intelligent conçu pour vous décharger de la gestion de vos emails. Avec IAcine_mail, les réponses générées sont automatiquement stockées dans vos brouillons, vous laissant le contrôle total quant à leur envoi final. Ce processus réduit considérablement votre charge mentale et le temps perdu sur des tâches répétitives.

Inspiré par des SaaS tels que Make, j'ai décidé de créer un outil open-source basé sur un seul script Python. Cette approche offre non seulement un véritable challenge, mais elle permet également une personnalisation, un contrôle, et une indépendance supérieurs par rapport à l'utilisation d'un SaaS payant.

![image](https://github.com/user-attachments/assets/0f85249b-79b8-42e3-98b3-d5f64ca59a24)


## Pré-requis pour utiliser IAcine_mail

- Un compte Gmail
- Un compte OpenAI avec une clé API active
- Un IDE pour exécuter le script Python (par exemple, VS Code, JupyterLab)

## Architecture de IAcine_mail

![image](https://github.com/user-attachments/assets/f131fec3-8db4-4a73-8942-9c6d23eed5ae)


## Étapes pour configurer et utiliser IAcine_mail

### Étape 1 : Créer un projet sur Google Cloud Platform

- Accédez à Google Cloud Platform.
- Créez un nouveau projet et sélectionnez-le.
![image](https://github.com/user-attachments/assets/e69ab587-a4d4-4ba6-8fcf-cff1cfeef3a4)

- Activez l'API Gmail.
![image](https://github.com/user-attachments/assets/187b6ccb-fa97-45eb-9f9a-3ff416acb687)

- Créez des identifiants en cliquant sur "Create Credentials" (suivez les screens suivants) :
    Type de compte : Desktop App
    Sélectionnez "User Data"
    Remplissez les informations comme requis
    Sautez l’étape "Scope" et finalisez en cliquant sur "Create"

![image](https://github.com/user-attachments/assets/931a77c3-7a2a-4488-8a6a-2a290af651da)
![image](https://github.com/user-attachments/assets/67d9b261-34cb-42c0-b935-dc77b081240d)
![image](https://github.com/user-attachments/assets/9d072af3-9296-4754-89bb-4536d5a22e87)
![image](https://github.com/user-attachments/assets/468c9f82-4599-4011-abac-6f11be882a96)

- Téléchargez votre Client ID généré :
![image](https://github.com/user-attachments/assets/2031e2e2-3fec-43cc-a86b-4ba8a4a7961d)


- Dans l'onglet "OAuth consent screen", ajoutez un utilisateur (utilisez le même email que précédemment) et sauvegardez.
![image](https://github.com/user-attachments/assets/c9944c65-c18b-4af1-a097-7e5c7c944146)

- Activez l'API Google People depuis le console GCP.
![image](https://github.com/user-attachments/assets/cd5f88fd-9991-4dca-a193-3692af6fad02)


Félicitations. Votre projet Google Cloud Platform est maintenant configuré !


### Étape 2 : Obtenez votre clé API OpenAI

Rendez-vous sur OpenAI API Keys (https://platform.openai.com/api-keys) et créez une nouvelle clé secrète. Assurez-vous d'avoir du crédit sur votre compte pour activer la clé.


### Étape 3 : Installation des dépendances et lancement du script

- Créez un environnement virtuel :
    Windows : python -m venv venv
    Linux : source venv/bin/activate
  
- Activez l'environnement :
        Windows : .\venv\Scripts\Activate
        Linux : source venv/bin/activate

- Installez les dépendances :
    Utilisez la commande : pip install -r requirements.txt

- Copiez le Client ID téléchargé dans un fichier nommé credentials.json :
    Utilisez la commande : cp 'C:\Users\XXXX\Downloads\client_secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json' credentials.json


Félicitations. Votre configuration est maintenant complète !


### Étape 4 : Lancer le script

- Exécutez le script et entrez "oui" :

![image](https://github.com/user-attachments/assets/1e0052f6-95f6-4c33-b21d-049128a797c7)

- Vous serez redirigé vers une page d'authentification Google.
  
![image](https://github.com/user-attachments/assets/b5fdc971-177c-4019-af4b-d7b29a73c523)



- Autorisez l'accès aux permissions nécessaires et cliquez sur "Continue" :

![image](https://github.com/user-attachments/assets/2925b50b-9e44-4bec-a71a-6c19653c80c1)


![image](https://github.com/user-attachments/assets/8b689e3f-948f-4f51-b40f-4c46087d134f)

![image](https://github.com/user-attachments/assets/85f2d375-9a5d-400c-a198-76e3cc971e38)




- Vous atterrirez sur la fenêtre suivante que vous pourrez quitter : 

![image](https://github.com/user-attachments/assets/8689637b-4bae-42b1-a8f6-e0442ff73233)


- Testez l'envoi d'un email :


Si aucun nouveau mail n'est reçu, le script vous en informera :
![image](https://github.com/user-attachments/assets/9e2b6e0f-77ef-4064-9ff8-8bbb8b34e05c)


Nous allons procéder à l’envoi d’un mail test depuis un autre compte Gmail :

![image](https://github.com/user-attachments/assets/502c8de6-53f6-44c8-8ca1-54c342a1adfc)


Après l’avoir envoyé, et l’avoir reçu sur notre boite mail :

![image](https://github.com/user-attachments/assets/8f82b201-e20a-4dd4-9772-1d19d12a386b)



Lorsqu'un email est reçu, le script génère une réponse automatiquement et la stocke dans vos brouillons.

![image](https://github.com/user-attachments/assets/159db520-8b81-4dca-aa7e-9e4f2bda4d04)

- Vérifiez les réponses dans vos brouillons, modifiez si nécessaire, puis envoyez. :
  
![image](https://github.com/user-attachments/assets/3497a4d6-1ef2-41fd-b74a-74bb0dd00fd2)

La réponse générée est de grande qualité et tout à fait conforme au résultat atteint si j’avais passé de longues minutes à devoir répondre à ce mail de test.



Conclusion

IAcine_mail est conçu pour vous simplifier la gestion de vos emails en automatisant la génération de réponses. Vous n'avez plus qu'à les valider avant de les envoyer, ce qui vous permet de rester organisé tout en gagnant du temps.

Pour toute question ou demande, contactez-moi directement sur LinkedIn :
LinkedIn - Yacine Mekideche (https://www.linkedin.com/in/yacine-mekideche/)



---------------------------------------------------------------------
© IAcine_mail 2024 - Yacine Mekideche. Tous droits réservés.
---------------------------------------------------------------------


