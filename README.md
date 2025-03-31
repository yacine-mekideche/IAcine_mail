# 📬 IAcine Mail | Intelligent Gmail Assistant with Local LLM  

![image](https://github.com/user-attachments/assets/15f5f5d1-e529-4a0e-aa6c-8ebe6e04e1c4)


## 📖 Introduction  

**IAcine Mail** is an intelligent Gmail assistant powered by a **local LLM (Llama 3.2:b)**. It automatically reads, analyzes, and generates professional replies to your unread Gmail messages — all while **preserving full data confidentiality** by processing everything **locally**.  

🚀 Designed to boost productivity and reduce email overload, IAcine Mail turns your inbox into a well-oiled machine.  

🔐 **Privacy-first:** No emails are ever sent to external servers.

## ⚙️ Features  

✔️ **Automated Email Retrieval** – Reads unread messages from your Gmail inbox  
✔️ **Smart Reply Generation** – Uses a local LLM to craft high-quality responses  
✔️ **Draft-Only Mode** – Replies are saved as Gmail drafts for manual review  
✔️ **OAuth 2.0 Integration** – Securely connects to your Google account  
✔️ **Terminal-based UI** – Lightweight and straightforward  
✔️ **Fully Local Execution** – Ensures complete data privacy  

## 🏗️ Technologies Used  

- 🐍 **Python 3.12** – Main language  
- 📩 **Google Gmail & People APIs** – For mail and user info access  
- 🛡️ **OAuth 2.0** – Authentication flow  
- 🧠 **Llama 3.2:b** – Local language model (via Docker)  
- 🎨 **pyfiglet + colorama** – For stylized console output  
- 📦 **openai** – (Optional) OpenAI GPT fallback  
- ⏳ **tqdm** – For progress indicators  


## 📦 Installation  

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/Yacine-Mekideche/iacine-mail.git
cd iacine-mail
```

### **2️⃣ Install the dependencies**
```bash
pip install -r requirements.txt
```

### **3️⃣ Add your credentials**
Download your OAuth 2.0 file from Google Cloud Console, and place it in the root of the project as:
```bash
credentials.json
```

☑️ Make sure to enable the following APIs in your GCP project:
Gmail API
People API

🔐 On first run, a browser will prompt you to log into your Gmail and authorize access. A token.pickle file will be created for future sessions.


## ▶️ Run the assistant

```bash
python API_mail2.py
```


Once authenticated, IAcine Mail will:

Scan your unread emails

Generate high-quality responses

Save them as drafts in your Gmail

🟢 Emails will not be sent automatically — you remain in control.



## Technical Architecture
![Diagramme sans nom drawio](https://github.com/user-attachments/assets/39932747-00c5-4176-a4e1-ceb7b6e26683)


## 🎯 Demo

<a href="https://www.youtube.com/watch?v=qel8LadCa8g" target="_blank">
  <img src="https://img.youtube.com/vi/qel8LadCa8g/maxresdefault.jpg" alt="IAcine Mail - Démonstration Vidéo" style="max-width:100%; height:auto;">
</a>



## 📬 Contact Me  

💡 **Let's connect! Whether you're interested in AI, Machine Learning, or tech collaborations, feel free to reach out.**  

[![Website](https://img.shields.io/badge/My%20Website-%23000000.svg?style=for-the-badge&logo=About.me&logoColor=white)](https://iacine.tech)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yacine-mekideche/)  
[![GitHub](https://img.shields.io/badge/GitHub-%2312100E.svg?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Yacine-Mekideche)  
[![Malt](https://img.shields.io/badge/Malt-%23FF6F61.svg?style=for-the-badge&logo=malt&logoColor=white)](https://malt.fr/profile/yacinemekideche)  
[![YouTube](https://img.shields.io/badge/YouTube-%23FF0000.svg?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@iacine_tech)  

📩 **Email for business inquiries:** contact@iacine.tech  

---

© 2025 IAcine. All rights reserved.
