# 🛡️ JobShield AI

### AI-Powered Fake Job & Internship Detection System

JobShield AI is a full-stack security analysis tool that helps students and job seekers identify potentially fraudulent job and internship opportunities **before** paying fees, sharing personal documents, or following suspicious links.

Instead of just saying "fake" or "real", it produces an **explainable 0–100 risk score**, lists every suspicious indicator with its detection source, verifies the company and recruiter email, and recommends the next action.

## 🌐 Live Demo

| | Link |
|---|---|
| **Web app** | https://jobshield-ai-4jq3.onrender.com |
| **API docs (Swagger)** | https://jobshield-ai-backend-fn0m.onrender.com/docs |
| **API health check** | https://jobshield-ai-backend-fn0m.onrender.com |

> ⏳ **Note:** The app runs on free hosting, which sleeps when idle. The **first load can take about a minute**; after that it responds normally.

## 📸 Screenshots

| High-risk result | Likely-genuine result |
|---|---|
| ![High risk](docs/screenshots/high-risk.png) | ![Likely genuine](docs/screenshots/likely-genuine.png) |

> Add your own screenshots to `docs/screenshots/` using the file names above.

---

## ✨ Key Features

### 🔍 Job Description Analysis
Paste a job or internship description. The system detects indicators such as:

- Registration or training fees and payment requests
- Unrealistic salary or income claims
- Guaranteed employment or placement
- Urgent application deadlines
- WhatsApp / Telegram-based communication
- Requests for sensitive personal information
- Threatening or intimidating language
- Suspicious recruiter email domains

### 🌐 Job URL Analysis
Submit a job-posting URL. JobShield AI fetches the page, extracts the readable text, removes unnecessary HTML, checks whether it is actually a job posting, and runs it through the same analysis pipeline.

### 🧠 NLP-Based Detection
Uses **spaCy** to catch suspicious employment language such as *guaranteed placement*, *100% placement*, *assured employment*, unrealistic income claims, sensitive-information requests and threatening language. NLP works alongside the rule-based engine to improve coverage.

### 📧 Recruiter Email Verification
Extracts recruiter emails and evaluates their domains. Free providers (Gmail, Yahoo, Outlook, Hotmail, ProtonMail) receive extra scrutiny. When a company website is available, the email domain is compared with the website domain, and a match (e.g. `careers@company.com` ↔ `company.com`) is treated as a stronger verification signal.

### 🏢 Company Verification
Identifies the company in the posting and checks the company name, website, recruiter email, email domain, website domain and shortened URLs. Shortened links (`lnkd.in`, `bit.ly`, `tinyurl.com`) are **not** treated as official company websites.

### 🔗 Verification Intelligence
Flags modern recruitment patterns that deserve a second look: shortened application URLs, applications that depend on social-media comments, third-party affiliation disclaimers and non-official application links. These signals do **not** automatically mean a scam; they move the result to *Needs Verification*.

### ⚪ Non-Job Detection
Content that is not a job posting (press releases, news articles, announcements, informational pages) is classified as **NOT A JOB POSTING**, so unrelated pages are never scored as scams.

### 📊 Risk Scoring & Classification

| Result | Meaning |
|---|---|
| 🟢 **LIKELY GENUINE** | No major scam indicators detected |
| 🟡 **NEEDS VERIFICATION** | Verification concerns were detected |
| 🔴 **HIGH RISK** | Multiple or severe scam indicators detected |
| ⚪ **NOT A JOB POSTING** | The content does not appear to be a job or internship |

### 🔎 Explainable Results
Every indicator shows its **points** and its **detection source** (Rule-Based, NLP, Email Analysis, Verification Intelligence, Website Verification).

```
🔴 HIGH RISK — Risk Score: 100/100

+25  Registration fee
+10  WhatsApp communication
+15  Guaranteed employment
+20  Sensitive personal information
+15  Attractive salary claim
+10  Threatening language
+10  Free email domain
```

### 💾 Analysis History
Every analysis is stored in PostgreSQL (ID, job text, risk score, risk level, company name, recommendation, timestamp) so users can review earlier checks.

---

## 🏗️ System Architecture

```
                  ┌──────────────────────┐
                  │        USER          │
                  └──────────┬───────────┘
                             ▼
                  ┌──────────────────────┐
                  │   React + Vite UI    │
                  │  (Render static site)│
                  └──────────┬───────────┘
                             │ REST (JSON)
                             ▼
                  ┌──────────────────────┐
                  │   FastAPI backend    │
                  │ (Docker, Render web) │
                  └──────────┬───────────┘
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
 ┌─────────────┐     ┌──────────────┐     ┌───────────────┐
 │ Rule-Based  │     │ NLP Analyzer │     │  URL Scraper  │
 │ Detection   │     │    spaCy     │     │ BeautifulSoup │
 └──────┬──────┘     └──────┬───────┘     └───────┬───────┘
        └───────────────────┼─────────────────────┘
                            ▼
                 ┌──────────────────────┐
                 │ Verification         │
                 │ Intelligence         │
                 │ Company / Email / URL│
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │  Risk Scoring 0–100  │
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │  Explainable Result  │
                 │ Risk + Flags + Advice│
                 └──────────┬───────────┘
                            ▼
                 ┌──────────────────────┐
                 │ PostgreSQL (Neon)    │
                 │   Analysis History   │
                 └──────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React, Vite, JavaScript, CSS |
| **Backend** | Python, FastAPI, Uvicorn |
| **AI / NLP** | spaCy (`en_core_web_sm`), pattern-based NLP analysis |
| **Web analysis** | Requests, BeautifulSoup |
| **Database** | PostgreSQL, psycopg2 |
| **DevOps** | Docker, Render (backend + frontend), Neon (managed PostgreSQL) |
| **Tools** | VS Code, Git, GitHub |

---

## 🚀 Deployment

| Component | Platform | Notes |
|---|---|---|
| Frontend (React + Vite) | Render (static site) | Reads the API address from `VITE_API_URL` |
| Backend (FastAPI) | Render (Docker web service) | Built from `backend/Dockerfile` |
| Database | Neon (PostgreSQL) | Connected through `DATABASE_URL` |

---

## 📁 Project Structure

```
JobShield-AI/
├── backend/
│   ├── main.py
│   ├── analyzer.py
│   ├── nlp_analyzer.py
│   ├── company_verifier.py
│   ├── job_scraper.py
│   ├── database.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .dockerignore
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── App.css
│   ├── package.json
│   └── vite.config.js
│
├── docs/
│   └── screenshots/
│
├── .gitignore
└── README.md
```

> The virtual environment (`venv`) and `.env` files are used locally only and must never be committed.

---

## ⚙️ Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/ramya938/JobShield-AI.git
cd JobShield-AI
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1          # Windows PowerShell
# source venv/bin/activate           # macOS / Linux
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 3. Database setup (PostgreSQL)

Create a database (locally, or a free one on [Neon](https://neon.com)) and run:

```sql
CREATE TABLE analysis_history (
    id SERIAL PRIMARY KEY,
    job_text TEXT NOT NULL,
    risk_score INTEGER NOT NULL,
    risk_level VARCHAR(50) NOT NULL,
    company_name VARCHAR(255),
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 4. Environment variables

Create `backend/.env`:

```env
# Option A: one connection string (used in production)
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DBNAME?sslmode=require

# Option B: separate local settings (used if DATABASE_URL is not set)
DB_HOST=localhost
DB_PORT=5432
DB_NAME=jobshield_db
DB_USER=postgres
DB_PASSWORD=YOUR_POSTGRES_PASSWORD

# Comma-separated list of frontend addresses allowed to call the API
ALLOWED_ORIGINS=http://localhost:5173
```

For the frontend, create `frontend/.env`:

```env
VITE_API_URL=http://127.0.0.1:8000
```

> 🔐 Never commit real passwords, connection strings or `.env` files to GitHub.

### 5. Start the backend

```bash
cd backend
uvicorn main:app --reload
```

API: http://127.0.0.1:8000 · Interactive docs: http://127.0.0.1:8000/docs

### 6. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

App: http://localhost:5173

### 🐳 Run the backend with Docker (optional)

```bash
cd backend
docker build -t jobshield-api .
docker run -p 8000:8000 -e DATABASE_URL="your_connection_string" jobshield-api
```

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API health / status |
| POST | `/analyze` | Analyze a job description |
| POST | `/analyze-url` | Analyze a job-posting URL |
| GET | `/history` | Retrieve previous analyses |

**Example request**

```bash
curl -X POST "https://jobshield-ai-backend-fn0m.onrender.com/analyze" \
  -H "Content-Type: application/json" \
  -d '{"job_text": "Pay a registration fee of Rs.500 to confirm your internship. Contact us on WhatsApp."}'
```

The response contains the risk score, risk level, red flags with sources, extracted emails and URLs, NLP findings, company verification, job detection and a recommendation.

---

## 🧪 Testing

The system was tested against three scenarios:

| Scenario | Contents | Result |
|---|---|---|
| 🔴 High-risk scam | Registration fee, WhatsApp contact, unrealistic salary, guaranteed employment, sensitive-data request, urgent deadline, Gmail recruiter address | **HIGH RISK, 100/100** |
| 🟢 Genuine-looking internship | Technical requirements, interview process, reasonable stipend, company-domain email, company website | **LIKELY GENUINE, 10/100** (company verification: STRONG) |
| 🟡 Social-media internship post | Shortened application URL, comment-based application, third-party disclaimer | **NEEDS VERIFICATION, 20/100** |

---

## 🔐 Security & Design Principles

- Suspicious indicators add to the risk score; verification concerns are kept separate from direct scam indicators.
- Shortened links are never treated as official company websites.
- Generic email domains receive extra scrutiny.
- Non-job content is separated from job-risk analysis.
- Results always come with explanations, not just a prediction.
- Secrets live in environment variables and are excluded from Git.

---

## 🔮 Future Improvements

- Machine-learning classification (TF-IDF + Logistic Regression) combined with the rule-based score
- LLM-powered risk explanations
- Domain reputation and WHOIS / domain-age analysis
- Trusted company verification APIs
- Browser extension
- Job-board integrations
- Email-based scam detection
- Screenshot / image-based job analysis
- User authentication and personalized history
- Automated tests and CI pipeline

---

## ⚠️ Disclaimer

JobShield AI is an assistive security-analysis tool, not a definitive fraud-verification service. A 🟢 **LIKELY GENUINE** result does not guarantee an opportunity is legitimate, and a 🟡 **NEEDS VERIFICATION** or 🔴 **HIGH RISK** result does not by itself prove fraud. Always verify the company, recruiter, website and application process independently before sharing sensitive information or making payments.

---

## 👩‍💻 Author

**Ramya Sri Penke**
B.Tech, Computer Science and Engineering (Cyber Security)

[LinkedIn](https://www.linkedin.com/in/ramya-sri-penke-713322292/) · [GitHub](https://github.com/ramya938) · [LeetCode](https://leetcode.com/u/Ramyasri006/) · [HackerRank](https://www.hackerrank.com/profile/23a31a4614)

---

## ⭐ Project Highlights

- Full-stack React + FastAPI application, deployed live
- Rule-based scam detection plus spaCy NLP analysis
- Recruiter email / domain and company verification
- URL analysis with web scraping
- Explainable 0–100 risk scoring with detection sources
- Non-job content detection
- PostgreSQL analysis history
- Dockerized backend with interactive API documentation
