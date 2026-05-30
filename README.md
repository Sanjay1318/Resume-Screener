# 🚀 Res Scanner ⚡

### AI-Powered Applicant Tracking System

<p align="center">
  <img src="https://img.shields.io/badge/Flask-Backend-black?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Groq-LLaMA%203-blueviolet?style=for-the-badge" />
  <img src="https://img.shields.io/badge/MySQL-Database-orange?style=for-the-badge&logo=mysql" />
  <img src="https://img.shields.io/badge/TailwindCSS-Frontend-38B2AC?style=for-the-badge&logo=tailwind-css" />
</p>

<p align="center">
  An advanced, enterprise-grade Applicant Tracking System (ATS) that evaluates resumes against job descriptions at lightning speed.
</p>

---

## ✨ Overview

**Res Scanner** utilizes **Groq's LLaMA 3 AI** for ultra-fast candidate evaluation, wrapped in a highly secure authentication system and a modern **"Aurora Glass"** dashboard experience.

The platform is designed to help recruiters and hiring teams efficiently analyze resumes, compare candidates, and visualize applicant strengths through interactive analytics.

---

# 🌟 Key Features

## ⚡ Ultra-Fast AI Evaluation

Powered by the **Groq API (LLaMA-3.3-70B)** to perform batch-processing of multiple resumes simultaneously, returning structured JSON evaluations in **1–2 seconds** with zero rate-limit crashing.

---

## 📊 Dual-Scoring Architecture

Calculates two distinct metrics:

* **AI Match Score** → Measures candidate impact, experience, and quality
* **ATS Score** → Measures keyword density and structural parseability

---

## 📈 Interactive Telemetry

Integrated with **Chart.js** to dynamically generate **Interactive Radar Charts** for every candidate, visualizing strengths across:

* Experience
* Education
* Skills
* Tech Depth

---

## 🔒 Enterprise-Grade Security

Includes:

* Password hashing with **Bcrypt**
* Secure session management using **Flask-Login**
* Custom **Two-Factor Authentication (2FA)** OTP flow via **Flask-Mail**

---

## 🎨 Premium UI/UX

Built using **Tailwind CSS** featuring:

* Custom **Cyber-Teal** color palette
* Frosted glassmorphism components
* Dynamic SVG circular progress gauges
* Smooth page transitions

---

## 📄 Smart Parsing & Export

Securely extracts text from PDFs using **pdfplumber** and allows recruiters to export complete Kanban-board scan results directly to CSV.

---

# 🛠️ Tech Stack

| Category                | Technologies                                                     |
| ----------------------- | ---------------------------------------------------------------- |
| **Backend**             | Python, Flask, SQLAlchemy, Flask-Login, Flask-Bcrypt, Flask-Mail |
| **AI Engine**           | Groq SDK (LLaMA 3)                                               |
| **Frontend**            | HTML5, Tailwind CSS, Chart.js, Jinja2                            |
| **Database**            | MySQL                                                            |
| **Document Processing** | pdfplumber, Werkzeug                                             |

---

# 🚀 Local Installation & Setup

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/Sanjay1318/Resume_Scanner.git
cd Resume_Scanner
```

---

## 2️⃣ Create & Activate Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux

```bash
python -m venv venv
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Configure Environment Variables

Create a `.env` file in the root directory and add the following credentials:

```env
SECRET_KEY=your_secure_secret_key
SQLALCHEMY_DATABASE_URI=mysql+pymysql://root:password@localhost/resume_scanner
GROQ_API_KEY=your_groq_api_key
MAIL_USERNAME=your.dedicated.app@gmail.com
MAIL_PASSWORD=your_16_character_app_password
```

> ⚠️ Note:
> This project enforces strict `.gitignore` rules for environment variables and sensitive credentials.

---

## 5️⃣ Initialize the Database

Ensure your **MySQL server** is running and the `resume_scanner` database is created.

---

## 6️⃣ Run the Application

```bash
python run.py
```

The application will be available at:

```bash
http://127.0.0.1:5000
```

---

# 🔒 Security & API Note

To run this project locally, you must:

* Supply your own **Groq API Key**
* Configure a dedicated **Gmail App Password** for SMTP OTP routing

---

# 📌 Future Improvements

* Resume ranking history
* Recruiter analytics dashboard
* AI interview question generation
* Candidate shortlisting automation
* Docker deployment support

---

# 👨‍💻 Author

### Vadla Sanjay Kumar

* GitHub: https://github.com/Sanjay1318
* LinkedIn: https://www.linkedin.com/in/sanjaychari007/

---

# ⭐ Support

If you found this project helpful, consider giving it a ⭐ on GitHub!
