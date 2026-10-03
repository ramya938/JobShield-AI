# 🛡️ JobShield AI

## AI-Powered Fake Job & Internship Detection System

JobShield AI is a full-stack security analysis system designed to help students and job seekers identify potentially fraudulent job and internship opportunities.

The system analyzes job descriptions and job-posting URLs using a combination of **rule-based detection, NLP analysis, recruiter email verification, company verification, URL analysis, and verification intelligence**.

Instead of simply declaring a job "fake" or "real", JobShield AI generates an explainable **0–100 risk score**, identifies suspicious indicators, provides company and recruiter verification information, and recommends the next action.

---

## ✨ Key Features

### 🔍 Job Description Analysis

Users can paste a job or internship description for analysis.

The system detects suspicious indicators including:

- Registration fees
- Training fees
- Payment requests
- Unrealistic salary or income claims
- Guaranteed employment or placement
- Urgent application deadlines
- WhatsApp/Telegram-based communication
- Requests for sensitive personal information
- Threatening or intimidating language
- Suspicious recruiter email domains

---

### 🌐 Job URL Analysis

Users can submit a job-posting URL.

JobShield AI:

1. Fetches the webpage
2. Extracts readable page content
3. Removes unnecessary HTML elements
4. Determines whether the content appears to be a job or internship posting
5. Sends the extracted content through the analysis pipeline
6. Generates an explainable risk assessment

---

### 🧠 NLP-Based Detection

The system uses **spaCy NLP** to identify suspicious employment-related patterns.

Examples include:

- Guaranteed job
- Guaranteed placement
- Guaranteed employment
- 100% placement
- Assured employment
- Unrealistic income claims
- Requests for sensitive information
- Threatening language

NLP detection works alongside rule-based detection to improve coverage of suspicious language patterns.

---

### 📧 Recruiter Email Verification

JobShield AI extracts recruiter email addresses and evaluates their domains.

It identifies commonly used free email providers such as:

- Gmail
- Yahoo
- Outlook
- Hotmail
- ProtonMail

When a company website is available, the system can compare the recruiter email domain with the company website domain.

For example:

```text
careers@company.com
matching:

company.com

provides a stronger verification signal.

🏢 Company Verification

The system attempts to identify the company mentioned in the posting and evaluate available verification information.

It checks:

Company name
Company website
Recruiter email
Email domain
Website domain
Shortened URLs

Shortened links such as lnkd.in, bit.ly, and tinyurl.com are not automatically treated as official company websites.

🔗 Verification Intelligence

JobShield AI includes additional verification signals for modern online recruitment patterns.

It can identify:

Shortened application URLs
Applications dependent on social-media comments
Third-party affiliation disclaimers
Non-official application links

These signals do not automatically mean that an opportunity is fraudulent.

Instead, they can cause the system to classify an opportunity as:

🟡 NEEDS VERIFICATION

⚪ Non-Job Detection

JobShield AI can identify content that does not appear to be a job or internship posting.

For example:

Company press releases
News articles
Corporate announcements
General informational pages

These are classified as:

⚪ NOT A JOB POSTING

This prevents unrelated webpages from being incorrectly scored as job scams.

📊 Risk Scoring

JobShield AI generates a risk score from:

0–100

The system uses four primary classifications:

Result	Meaning
🟢 LIKELY GENUINE	No major scam indicators detected
🟡 NEEDS VERIFICATION	Verification concerns were detected
🔴 HIGH RISK	Multiple or severe scam indicators were detected
⚪ NOT A JOB POSTING	The analyzed content does not appear to be a job or internship

The score is based on multiple detection sources rather than a single rule.

🔎 Explainable Detection

JobShield AI does not only return a prediction.

It explains why the opportunity received its risk score.

Each detected indicator identifies its detection source, such as:

Rule-Based
NLP
Email Analysis
Verification Intelligence
Website Verification
Example
🔴 HIGH RISK

Risk Score: 100/100

Risk Indicators:

+25 Registration fee
+10 WhatsApp communication
+15 Guaranteed employment
+20 Sensitive personal information
+15 Attractive salary claim
+10 Threatening language
+10 Free email domain

This makes the result easier for users to understand and verify.
System Architecture
                         ┌──────────────────────┐
                         │        USER          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   React Frontend     │
                         │                      │
                         │ Job Text / URL Input │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     FastAPI API      │
                         └──────────┬───────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
      ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
      │ Rule-Based    │     │ NLP Analyzer  │     │  URL Scraper  │
      │ Detection     │     │    spaCy      │     │ BeautifulSoup │
      └───────┬───────┘     └───────┬───────┘     └───────┬───────┘
              │                     │                     │
              └─────────────────────┼─────────────────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Verification         │
                         │ Intelligence         │
                         │                      │
                         │ Company / Email / URL│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Risk Scoring      │
                         │       0–100          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Explainable Result   │
                         │                      │
                         │ Risk + Red Flags +   │
                         │ Verification + Advice│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     PostgreSQL       │
                         │   Analysis History   │
                         └───────────────────


┘
🛠️ Technology Stack
Frontend
React
Vite
JavaScript
CSS
Backend
Python
FastAPI
Uvicorn
AI / NLP
spaCy
en_core_web_sm
Pattern-based NLP analysis
Web Analysis
Requests
BeautifulSoup
Database
PostgreSQL
psycopg2
Development Tools
VS Code
Git
GitHub
📁 Project Structure
JobShield-AI/
│
├── backend/
│   ├── main.py
│   ├── analyzer.py
│   ├── nlp_analyzer.py
│   ├── company_verifier.py
│   ├── job_scraper.py
│   ├── database.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
│
├── .gitignore
└── README.md

The Python virtual environment (venv) is used locally and should not be committed to GitHub.

⚙️ Installation & Setup
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/JobShield-AI.git
cd JobShield-AI
🐍 Backend Setup

Navigate to the backend:

cd backend

Create a virtual environment:

python -m venv venv

Activate the environment on Windows:

.\venv\Scripts\Activate.ps1

Install the dependencies:

pip install -r requirements.txt

Download the spaCy English model:

python -m spacy download en_core_web_sm
🗄️ PostgreSQL Setup

Create the database:

CREATE DATABASE jobshield_db;

Connect to the database and create the analysis history table:

CREATE TABLE analysis_history (
    id SERIAL PRIMARY KEY,
    job_text TEXT NOT NULL,
    risk_score INTEGER NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    company_name VARCHAR(255),
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
🔐 Environment Variables

Create a .env file inside the backend directory:

DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobshield_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD
Important

Never commit your real .env file or PostgreSQL password to GitHub.

▶️ Running the Backend

From the backend directory:

uvicorn main:app --reload

The API will be available at:

http://127.0.0.1:8000

FastAPI interactive documentation:

http://127.0.0.1:8000/docs
💻 Running the Frontend

Open a second terminal.

Navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

Open the application:

http://localhost:5173
🔌 API Endpoints
Method	Endpoint	Purpose
GET	/	API health/status
POST	/analyze	Analyze job description
POST	/analyze-url	Analyze job-posting URL
GET	/history	Retrieve previous analyses

FastAPI automatically provides interactive API documentation at:

http://127.0.0.1:8000/docs
🧪 Testing

The system was tested against three different scenarios.

🔴 Test 1 — High-Risk Scam

A simulated internship containing:

Registration fee
WhatsApp communication
Unrealistic salary
Guaranteed employment
Sensitive personal information request
Urgent deadline
Gmail recruiter address
Result
🔴 HIGH RISK
100/100
🟢 Test 2 — Genuine-Looking Internship

A simulated software development internship containing:

Technical requirements
Interview process
Reasonable stipend
Company-domain recruiter email
Company website
Result
🟢 LIKELY GENUINE
10/100

The recruiter email domain matched the company website domain, resulting in:

Company Verification: STRONG
🟡 Test 3 — Social-Media Internship Post

A simulated Cognizant-related internship post containing:

Shortened application URL
Social-media comment-based application
Third-party affiliation disclaimer
Result
🟡 NEEDS VERIFICATION
20/100

The system correctly identified verification concerns without automatically declaring the opportunity fraudulent.

💾 Analysis History

JobShield AI stores previous analyses in PostgreSQL.

The history includes:

Analysis ID
Job description
Risk score
Risk level
Company name
Recommendation
Analysis timestamp

This allows users to review previously analyzed opportunities.

🔐 Security Considerations

JobShield AI is designed as an assistive security-analysis tool.

The system follows a conservative approach:

Suspicious indicators contribute to the risk score.
Verification concerns are separated from direct scam indicators.
Shortened links are not treated as official company websites.
Generic email domains receive additional scrutiny.
Non-job content is separated from job-risk analysis.
Results include explanations rather than unexplained predictions.
🎯 Project Objective

The primary objective of JobShield AI is to help students, fresh graduates, and job seekers identify potentially fraudulent employment opportunities before:

Paying recruitment fees
Sharing sensitive personal information
Following suspicious application links
Communicating with potentially fraudulent recruiters

The system provides an additional layer of analysis and encourages users to independently verify important employment information.

🔮 Future Improvements

Possible future enhancements include:

Machine-learning-based classification
LLM-powered risk explanations
Domain reputation analysis
WHOIS/domain-age analysis
Trusted company verification APIs
Browser extension
Job-board integrations
Email-based scam detection
Screenshot/image-based job analysis
Threat-intelligence feeds
Cloud deployment
User authentication
Personalized risk history
⚠️ Disclaimer

JobShield AI is an assistive security-analysis system and should not be considered a definitive fraud-verification service.

A:

🟢 LIKELY GENUINE

result does not guarantee that an opportunity is legitimate.

Similarly:

🟡 NEEDS VERIFICATION

or:

🔴 HIGH RISK

does not independently prove fraud.

Users should independently verify the company, recruiter, website, and application process before sharing sensitive information or making payments.

👩‍💻 Author

Ramya Sri

Built as a full-stack AI/NLP security project focused on helping students and fresh graduates identify potentially fraudulent job and internship opportunities.

⭐ Project Highlights
Full-stack React + FastAPI application
Rule-based scam detection
NLP-powered suspicious-language detection
Recruiter email/domain verification
Company verification
URL analysis and web scraping
Verification intelligence
Explainable 0–100 risk scoring
Non-job content detection
PostgreSQL analysis history
Interactive FastAPI API documentation

