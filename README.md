# Res Scanner ⚡ | AI-Powered Resume Analyzer

An advanced, AI-driven application designed to streamline the recruitment process. Res Scanner evaluates resumes against job descriptions using Google's Gemini AI, wrapped in a highly secure, production-grade authentication system and a modern "Aurora Glass" UI.

## ✨ Key Features

* **AI Resume Evaluation:** Integrates with the Google Gemini API to parse, analyze, and score candidate resumes against specific job requirements.
* **Enterprise-Grade Security:** Features robust password hashing using `Bcrypt` and secure session management via `Flask-Login`.
* **Two-Factor Authentication (2FA):** Implements a custom One-Time Password (OTP) flow utilizing `Flask-Mail` and Google's SMTP servers to dispatch 6-digit verification codes to users upon login.
* **Account Recovery System:** Complete self-service password reset flow (Forgot Password -> OTP Verification -> Reset) mirroring modern SaaS standards.
* **Premium UI/UX:** Built with TailwindCSS featuring a bespoke "Cyber-Teal" color palette, frosted glassmorphism elements, and smooth page transitions.
* **Relational Database:** Powered by MySQL and SQLAlchemy to securely store user credentials, temporary OTP tokens, and historical scan data.

## 🛠️ Tech Stack

* **Backend:** Python, Flask, Flask-SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Mail
* **Frontend:** HTML5, TailwindCSS, Jinja2 Templating
* **Database:** MySQL
* **AI Integration:** Google Gemini API

## 🚀 Local Installation & Setup

**1. Clone the repository**
```bash
git clone [https://github.com/YourUsername/Resume_Scanner.git](https://github.com/YourUsername/Resume_Scanner.git)
cd Resume_Scanner
2. Create and activate a virtual environment

Bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
3. Install dependencies

Bash
pip install -r requirements.txt
4. Environment Variables
Create a .env file in the root directory and add your secure credentials. (Note: Never commit this file to version control).

Plaintext
SECRET_KEY=your_secure_secret_key
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password@localhost/resume_scanner
GEMINI_API_KEY=your_google_gemini_api_key
MAIL_USERNAME=your.dedicated.app@gmail.com
MAIL_PASSWORD=your_16_character_app_password
5. Initialize the Database
Ensure your MySQL server is running and the resume_scanner database is created.

6. Run the Application

Bash
python run.py
The application will be available at http://127.0.0.1:5000

🔒 Security Note
This repository strictly ignores environment variables and API keys. To run this project locally, you must supply your own Google Gemini API key and configure a dedicated Gmail App Password for SMTP routing.