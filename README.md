#  English Learning App

An AI-powered English Learning Platform designed to enhance English communication skills through interactive quizzes, AI-generated questions, pronunciation support, and real-time chat functionality.

##  Overview

The English Learning App helps learners improve their vocabulary, grammar, listening, and communication skills using modern AI technologies. The platform combines adaptive quizzes, text-to-speech, and live interaction features to create an engaging learning experience.

---

## ✨ Key Features

###  Interactive Quiz System

* Topic-based English quizzes
* Dynamic question generation
* Instant answer evaluation
* Hint-based learning support
* Performance tracking through attempts

### 🤖 AI-Generated Questions

* Powered by Groq AI (Llama 3.3 70B)
* Automatically generates unique English questions
* Supports multiple topics and difficulty levels
* Uses Excel datasets as learning resources

### 🔊 Text-to-Speech Support

* Converts questions into audio
* Improves pronunciation and listening skills
* Built using Google Text-to-Speech (gTTS)

### 💬 Real-Time Chat

* WebSocket-based live chat
* Interactive communication environment
* Instant message broadcasting

### 📚 Learning Resources

* Excel-based question datasets
* AI-assisted content generation
* Continuous question expansion

---

## 🏗️ System Architecture

```text
Frontend (Streamlit)
        │
        ▼
Backend (FastAPI)
        │
 ┌──────┼──────┐
 ▼      ▼      ▼
MySQL  Groq AI  gTTS
Database  API   Audio Service
```
## Image

<img width="576" height="398" alt="image" src="https://github.com/user-attachments/assets/376d9172-6c9a-42f3-9b0d-5d653fea042e" />


<img width="589" height="376" alt="image" src="https://github.com/user-attachments/assets/bfbbe6e6-27ad-4d57-95bd-6070b4b71b57" />

---

## 🛠️ Technology Stack

### Frontend

* Streamlit
* HTML
* CSS
* JavaScript

### Backend

* FastAPI
* WebSockets
* SQLAlchemy

### Database

* MySQL

### AI & NLP

* Groq API
* Llama 3.3 70B Versatile

### Additional Libraries

* gTTS
* OpenPyXL
* Pydantic
* Uvicorn

---

## 📂 Project Structure

```text
English-Learning-App/
│
├── app.py
├── main.py
├── config.py
├── db.py
├── models.py
├── schemas.py
├── services.py
├── groq_service.py
├── tts_service.py
├── excel_loader.py
├── requirements.txt
├── .env
│
├── static/
│   ├── audio files
│   └── assets
│
└── data/
    └── Excel datasets
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/Hariom-patidar-tech/english-learning-application.git
cd english-learning-application
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
DATABASE_URL=your_database_url
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_groq_api_key
```

---

## ▶️ Run FastAPI Backend

```bash
uvicorn main:app --reload --port 8001
```

API Documentation:

```text
http://127.0.0.1:8001/docs
```

---

## ▶️ Run Streamlit Frontend

```bash
streamlit run app.py
```

Application URL:

```text
http://localhost:8501
```

---

## 🎯 Learning Outcomes

* Improve English vocabulary
* Strengthen grammar fundamentals
* Enhance listening comprehension
* Practice English communication
* Learn through AI-assisted interaction

---

## 🔮 Future Enhancements

* User Authentication & Profiles
* Progress Analytics Dashboard
* Speaking Practice Module
* AI Conversation Partner
* Leaderboard & Gamification
* Personalized Learning Paths
* Advanced Grammar Correction

---

## 👨‍💻 Developer

**Hariom Patidar**

AI/ML & Data Science Enthusiast

**Skills:** Python, Machine Learning, Deep Learning, FastAPI, Generative AI, Data Science

---

## ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
