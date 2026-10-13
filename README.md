# 🛡️ ScamShield – Scam Detection System

ScamShield is a web-based scam detection project designed to help users identify suspicious messages, website URLs, and YouTube video claims.

## 🚀 Features

- **Message Scam Detection:** Checks messages for common scam phrases and warning signs.
- **Website URL Checking:** Identifies basic URL warning signs, such as IP-address URLs and non-HTTPS links.
- **YouTube Video Claim Checking:** Checks YouTube video links and user-provided claims for configured warning phrases.
- **Clear Results:** Returns a verdict and reasons to help users understand the results.
- **FastAPI Backend:** Provides API endpoints for scam checking.

## 🛠️ Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Requests
- HTML

## 📂 Project Structure

```text
scamshield/
├── app.py
├── templates/
│   └── index.html
├── requirements.txt
└── README.md
```

## ⚙️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/keerthigandrothu/scamshield.git
   ```

2. Open the project folder:

   ```bash
   cd scamshield
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the FastAPI server:

   ```bash
   uvicorn app:app --reload
   ```

5. Open the API documentation in your browser:

   http://127.0.0.1:8000/docs

## 🔗 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Check whether the backend is running |
| POST | `/check` | Check a text message |
| POST | `/check-url` | Check a website URL |
| POST | `/check-video` | Check a YouTube video claim |

## ⚠️ Disclaimer

ScamShield uses configured warning phrases and basic URL checks. It cannot detect every scam or guarantee that a message, website, or video is safe or genuine.

Always verify important information through official sources. Do not share passwords, banking details, or OTPs with untrusted people or websites.

## 🎯 Project Goal

The goal of ScamShield is to help users recognize potential online scams and make more informed decisions about suspicious messages, links, and video claims.
