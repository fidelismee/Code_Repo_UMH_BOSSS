# 🚗 BOSSS – **B**ert-powered **O**nboard **S**peech **S**upport **S**ystem  
### ✨ A Voice Assistant for Grab Driver-Partners (DAX) | UMHackathon 2025

![Python](https://img.shields.io/badge/Made%20with-Python-blue.svg)
![Flask](https://img.shields.io/badge/Framework-Flask-orange.svg)
![NLP](https://img.shields.io/badge/NLP-DistilBERT-brightgreen.svg)

---

## 📌 Introduction

**BOSSS** is a GenAI-powered voice assistant designed specifically for **Grab's driver-partners (DAX)** to provide hands-free, safe, and intelligent support while driving. Developed for **UMHackathon 2025**, BOSSS is tailored to operate in **noisy, real-world driving environments**—enabling drivers to interact via natural speech to get directions, perform tasks like calling or rejecting customers, and much more.

The solution aligns with Grab’s mission of *economic empowerment through AI*, leveraging speech recognition and natural language understanding to automate tasks, reduce distractions, and keep hands on the wheel.

---

## 🚀 Features

✅ **Hands-free Voice Control**  
✅ **Intent Recognition using fine-tuned DistilBERT**  
✅ **Speech-to-Text (Google Speech Recognition)**  
✅ **Noise Tolerant Interaction**  
✅ **Natural Language → Structured JSON Mapping**  
✅ **Voice Response (pyttsx3)**  
✅ **GUI using Tkinter for easy interaction**  

---

## 💡 How It Works (Full Flow)

1. 🎙 **Driver Speaks**  
2. 🧠 `speech_button_client.py` captures and converts speech to text  
3. 📡 Sends the text to `app.py` → `/classify`  
4. 🤖 DistilBERT predicts the user **intent**  
5. 📡 Sends the intent to `forward_intent_server.py` → `/process`  
6. 🔧 JSON output is returned for downstream processing  
7. 🔊 Response is read aloud using `pyttsx3`

---

## 🛠️ Setup Instructions

```bash
git clone https://github.com/your-username/Code_Repo_UMH_BOSSS.git
cd Code_Repo_UMH_BOSSS/src
```

### 🔧 Install via pip:
```bash
pip install flask
pip install transformers
pip install torch
pip install scikit-learn
pip install speechrecognition
pip install pyttsx3
pip install requests
```

### Terminal 1
```
python app.py
```

### Terminal 2
```
python forward_intent_server.py
```

### Terminal 3
```
python speech_button_client.py
```

## 🎥 Video Demonstration & Slides

📽 **Video Prototype:**  
[🔗 Watch on Google Drive](https://drive.google.com/file/d/1QvTKSWhwdZrEMk55Zhcx_Jz2DTCGbE6n/view?usp=drivesdk)

📊 **Presentation Slides:**  
[🔗 View on Google Drive](https://drive.google.com/file/d/1zAuMjN91N44DMsjftRTqvxZFC_kcO0qs/view?usp=drive_link)





