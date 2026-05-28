# Res Scanner ⚡

Res Scanner is an advanced, production-grade AI application designed to intelligently parse, analyze, and categorize candidate resumes against specific Job Descriptions.

Transitioning from a basic local-file script to a secure, scalable SaaS architecture, this tool leverages Google's Gemini Large Language Models to read resumes, identify skill gaps, and provide actionable hiring telemetry. The frontend features a highly customized, premium "Cyber-Teal" dark mode aesthetic.

## 🌟 Key Features

* **Intelligent AI Parsing:** Utilizes Google's Gemini LLM (via the `google-genai` SDK and models like `gemini-2.0-flash`) to evaluate candidate profiles.
* **Automated Categorization:** Automatically scores candidates out of 100% and organizes them into a Kanban-style board with "Priority" (>85%), "Shortlisted" (65-85%), and "Rejected" (<65%) buckets.
* **Deep AI Telemetry:** Generates concise 2-sentence candidate summaries, evaluates experience matches, identifies missing skills from the JD, and suggests custom interview questions.
* **Flexible Inputs:** Accepts Job Descriptions via raw text pasting or direct `.txt`/`.pdf` document uploads.
* **Bulk Processing:** Upload and scan up to 30 candidate resumes at once, strictly enforced on both the frontend and backend to protect system performance.
* **Premium UI/UX:** Features a custom "Cyber-Teal" glassmorphic design built with Tailwind CSS, including a dynamic, animated neon progress track during AI processing.
* **System Analytics Dashboard:** Tracks operational metrics such as total batches run, total resumes processed, and priority hires identified.
* **Data Portability:** Includes a one-click CSV export feature to download the generated AI analysis into a spreadsheet.
* **Secure User Authentication:** Full account system using Flask-Login and Bcrypt, ensuring candidate data is strictly tied to individual recruiter accounts.

---

## 🛠️ Tech Stack

**Backend**

* Python 3.x
* Flask (Web Framework)
* SQLAlchemy (ORM)
* Flask-Login & Flask-Bcrypt (Authentication & Security)

**Database**

* MySQL
* PyMySQL & Cryptography (Database Drivers)

**AI & Document Processing**

* Google Generative AI SDK (`google-genai`)
* `pdfplumber` (PDF text extraction)

**Frontend**

* HTML5 / Jinja2 Templating
* Tailwind CSS (via CDN)
* HTMX (Concepts integrated for dynamic UI elements)

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/res-scanner.git
cd res-scanner

```

### 2. Set Up a Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install Flask Flask-SQLAlchemy Flask-Login Flask-Bcrypt PyMySQL cryptography pdfplumber google-genai

```

### 4. Database Configuration

1. Ensure you have a local MySQL server running.
2. Create an empty database named `resume_scanner`.
3. Create a `config.py` file in the root directory and add your MySQL URI and Google Gemini API key:

```python
class Config:
    SECRET_KEY = 'your-secure-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/resume_scanner'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = 'resume_uploads'
    GEMINI_API_KEY = 'your-google-gemini-api-key'

```

*(Note: Replace `username`, `password`, and the API key with your actual credentials)*.

### 5. Run the Application

The SQLAlchemy ORM will automatically generate the required database tables (`users`, `scans`, `resumes`) the first time the application runs.

```bash
python run.py

```

Open your browser and navigate to `[http://127.0.0.1:5000](http://127.0.0.1:5000)`.

---

## 🖥️ Usage Guide

1. **Create an Account:** Start by registering a new user account to access the secure system lock.
2. **Initialize Evaluation:** From the main dashboard, enter a Target Job Title and provide the Job Description.
3. **Upload Telemetry:** Select up to 30 candidate `.pdf` or `.txt` files and click "Initialize Evaluation".
4. **Review Matrix:** Wait for the AI to process the batch. Once complete, you will be redirected to the Evaluation Matrix to view candidate scores and expand individual AI Telemetry cards.
5. **Manage Data:** Use the "System Analytics" tab to review your historical processing logs, export past scans to CSV, or permanently purge old scan matrices.