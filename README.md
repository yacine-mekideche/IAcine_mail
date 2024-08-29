# IAcine_mail: Your Gmail AI-ssistant at your fingertips! 📩

![image](https://github.com/user-attachments/assets/67dbd647-5b10-4a37-83ac-714d9187388c)


## Introduction
Daily email management can quickly become a tedious task, turning our inbox into a cluttered and disorganized space.
Many of us dream of an empty inbox at the end of the day, but it often seems out of reach.

It is from this frustration that the idea of ​​creating IAcine_mail was born: an intelligent assistant designed to relieve you of the management of your emails.
With IAcine_mail, the generated responses are automatically stored in your drafts, giving you full control over their final sending.

This process significantly reduces your mental load and the time wasted on repetitive tasks.

Inspired by automation SaaS like Make, I decided to create an open-source tool based on a single Python script.
This approach not only offers a real challenge, but it also allows for greater customization, control, and independence compared to using a paid SaaS.

![image](https://github.com/user-attachments/assets/0ea640e0-bec1-4c29-861b-51f8e5e7da46)



## Prerequisites to use IAcine_mail

- A Gmail account
- An OpenAI account with an active API key
- An IDE to run the Python script (e.g. VS Code, JupyterLab)

## Architecture of IAcine_mail
![image](https://github.com/user-attachments/assets/28ab41df-26c1-442d-8df7-e16722383842)





## Steps to configure and use IAcine_mail

### Step 1: Create a project on Google Cloud Platform

- Enable Gmail API.

![image](https://github.com/user-attachments/assets/032688b8-f06b-4ed1-9c11-41faf48dd494)



- Create credentials by clicking on "Create Credentials" (follow the following screens):

  `Account Type: Desktop App`
  
  `Select "User Data"`
  
  `Fill in the information as required`
  
  `Skip the "Scope" step and finalize by clicking on "Create"`

![image](https://github.com/user-attachments/assets/3da3e6ff-f851-4d95-9156-3483df1d0a76)

![image](https://github.com/user-attachments/assets/b6fbd885-b25e-44a3-a321-7870ccb9d192)

![image](https://github.com/user-attachments/assets/026598f7-c3e5-4be9-bfd7-3ccbd157e167)

![image](https://github.com/user-attachments/assets/c73e6f2c-0cc8-47ef-a7ae-f81d7244d1c3)


- Download your generated Client ID:

![image](https://github.com/user-attachments/assets/a845712e-e168-4282-a1bd-45a8095e9a4f)


- In the "OAuth consent screen" tab, add a user (use the same email as before) and save :

![image](https://github.com/user-attachments/assets/4ada182f-9952-4d36-890a-363101c66206)


- Enable Google People API from the GCP console.

![image](https://github.com/user-attachments/assets/65824332-aa61-4017-b222-ec2f5d0ff8bd)


Congratulations! 🎉 Your Google Cloud Platform project is now set up!


### Step 2: Get your OpenAI API Key

Go to OpenAI API Keys (https://platform.openai.com/api-keys) and create a new secret key. 

Make sure you have credit on your account to activate the key.


### Step 3: Installing dependencies and running the script

- Download the following files :

`API_mail.py`

`requirements.txt`

- Create a virtual environment; run the following command :

```
python -m venv venv
```

  
- Activate the environment; run the following command :

Windows:
```
.\venv\Scripts\Activate
```

Linux: 
```
source venv/bin/activate
```



- Install the dependencies; run the following command :

```
pip install -r requirements.txt
```

- Copy the downloaded Client ID into a file named credentials.json; run the following command :

```
cp 'C:\Users\XXXX\Downloads\client_secret_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.apps.googleusercontent.com.json' credentials.json
```

Congratulations! 🎉 Your setup is now complete!


### Step 4: Run the script

- Run the script and enter "oui":

![image](https://github.com/user-attachments/assets/5a14da2d-3338-4347-9dc7-b108451251cc)


- You will be redirected to a Google authentication page :
  
![image](https://github.com/user-attachments/assets/5608918d-4ea3-4e0b-a6b0-63ff8cd6fbb0)




- Allow access to the necessary permissions and click "Continue" :

![image](https://github.com/user-attachments/assets/b19c671f-f3c1-4afa-b541-00763a669ddf)

![image](https://github.com/user-attachments/assets/d6a6c03e-11c5-440e-86aa-87dc8bc5bc83)

![image](https://github.com/user-attachments/assets/377ac6d5-e8a8-4aec-8f0b-b904ed00b202)





- You will see the following window that you can exit:

![image](https://github.com/user-attachments/assets/e2221fae-92cd-4fe9-b030-66ab410e65a6)



- Test sending an email:


If no new email is received, the script will inform you:

![image](https://github.com/user-attachments/assets/429111f3-15cc-45db-b3b6-a247312af527)


We will proceed to send a test email from another Gmail account:

![image](https://github.com/user-attachments/assets/502c8de6-53f6-44c8-8ca1-54c342a1adfc)


After sending it, and receiving it on our mailbox :

![image](https://github.com/user-attachments/assets/8f82b201-e20a-4dd4-9772-1d19d12a386b)



When an email is received, the script generates a reply automatically and stores it in your drafts.

![image](https://github.com/user-attachments/assets/159db520-8b81-4dca-aa7e-9e4f2bda4d04)

- Check the replies in your drafts, edit if necessary, then send :
  
![image](https://github.com/user-attachments/assets/e05978e8-96a1-4449-a863-5421f0ef5b94)



## Conclusion

The response generated is of high quality and completely consistent with the result achieved if I had spent long minutes having to respond to this test email.

IAcine_mail is designed to simplify the management of your emails by automating the generation of responses. You only have to validate them before sending them, which allows you to stay organized while saving time.

For any questions or requests, please contact me directly on LinkedIn: https://www.linkedin.com/in/yacine-mekideche/.



---------------------------------------------------------------------
© IAcine_mail 2024 - Yacine Mekideche. All rights reserved.
---------------------------------------------------------------------


