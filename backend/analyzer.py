import re
import requests
from urllib.parse import urlparse
from nlp_analyzer import analyze_with_nlp
from company_verifier import verify_company

# ==========================================
# Rule-Based Scam Indicators
# ==========================================
RED_FLAGS = {
    "registration fee": 25,
    "registration fees": 25,
    "training fee": 20,
    "training fees": 20,
    "pay to apply": 25,
    "payment required": 25,
    "whatsapp": 10,
    "telegram": 10,
    "urgent": 10,
    "immediately": 5,
    "limited seats": 5,
    "guaranteed job": 15,
    "guaranteed placement": 15,
    "work from home": 3,
}

# ==========================================
# Negation-Aware Matching (payment keywords)
# ==========================================
NEGATABLE_FLAGS = {
    "registration fee",
    "registration fees",
    "training fee",
    "training fees",
    "pay to apply",
    "payment required",
}

# "no registration fee", "without any fee", "don't pay to apply"
NEG_BEFORE = re.compile(
    r"\b(?:no|not|without|zero|never|nor|free of|don't|dont|do not)\b"
    r"(?:\s+\w+){0,2}\s*$"
)

# "registration fee is not required", "fee isn't charged", "fee is free"
NEG_AFTER = re.compile(
    r"^\s*(?:(?:is|are|will be|be|was)\s+)?"
    r"(?:not|never|no|isn't|aren't)\s+(?:be\s+)?"
    r"(?:required|needed|necessary|charged|applicable|collected|applied)"
    r"|^\s*(?:is|are)\s+(?:free|waived)\b"
)


def is_negated(text_lower, start, end):
    # Look a few words before the match (same clause only)
    before = text_lower[max(0, start - 40):start]
    before = re.split(r"[.,;:!?\n]", before)[-1]

    # Look a few words after the match (same clause only)
    after = text_lower[end:end + 40]
    after = re.split(r"[.,;:!?\n]", after)[0]

    return bool(NEG_BEFORE.search(before) or NEG_AFTER.match(after))


def has_non_negated(text_lower, keyword):
    """True if the keyword appears at least once WITHOUT being negated."""
    pattern = r"\b" + re.escape(keyword) + r"\b"
    for match in re.finditer(pattern, text_lower):
        if not is_negated(text_lower, match.start(), match.end()):
            return True
    return False


# ==========================================
# Free Email Providers
# ==========================================
FREE_EMAIL_DOMAINS = {
    "gmail.com",
    "yahoo.com",
    "outlook.com",
    "hotmail.com",
    "protonmail.com",
}

# ==========================================
# Job / Internship Detection Keywords
# ==========================================
JOB_KEYWORDS = [
    "job",
    "jobs",
    "career",
    "careers",
    "vacancy",
    "vacancies",
    "hiring",
    "hire",
    "recruitment",
    "recruiting",
    "employment",
    "position",
    "positions",
    "role",
    "roles",
    "internship",
    "internships",
    "intern",
    "developer",
    "engineer",
    "software developer",
    "software engineer",
    "data analyst",
    "data scientist",
    "application",
    "apply now",
    "apply",
    "job description",
    "qualifications",
    "responsibilities",
    "candidate",
    "candidates",
    "salary",
    "stipend",
    "experience",
    "work location",
    "full time",
    "part time",
]

# ==========================================
# Non-Job Webpage Keywords
# ==========================================
NON_JOB_KEYWORDS = [
    "press release",
    "news",
    "newsroom",
    "article",
    "blog",
    "blog post",
    "latest news",
    "investor relations",
    "financial results",
    "quarterly results",
    "shareholder",
    "media center",
    "company announcement",
]

# ==========================================
# Extract Email Addresses
# ==========================================
def extract_emails(text):
    return re.findall(
        r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
        text
    )

# ==========================================
# Extract URLs
# ==========================================
def extract_urls(text):
    return re.findall(
        r"https?://[^\s]+",
        text
    )

# ==========================================
# Analyze Email Addresses
# ==========================================
def analyze_emails(emails):
    email_analysis = []

    for email in emails:
        domain = email.split("@")[-1].lower()

        if domain in FREE_EMAIL_DOMAINS:
            email_analysis.append({
                "email": email,
                "domain": domain,
                "status": "SUSPICIOUS",
                "reason": "Recruiter is using a free email provider."
            })
        else:
            email_analysis.append({
                "email": email,
                "domain": domain,
                "status": "COMPANY DOMAIN",
                "reason": "Email uses a custom domain."
            })

    return email_analysis

# ==========================================
# Analyze URLs
# ==========================================
def analyze_urls(urls):
    url_analysis = []

    for url in urls:
        clean_url = url.rstrip(".,)")

        try:
            domain = urlparse(clean_url).netloc.lower()

            url_analysis.append({
                "url": clean_url,
                "domain": domain
            })
        except Exception:
            pass

    return url_analysis

# ==========================================
# Verify Website
# ==========================================
def verify_website(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            allow_redirects=True
        )

        return {
            "url": url,
            "final_url": response.url,
            "domain": urlparse(response.url).netloc.lower(),
            "reachable": True,
            "status_code": response.status_code
        }

    except requests.RequestException:
        return {
            "url": url,
            "domain": urlparse(url).netloc.lower(),
            "reachable": False,
            "status_code": None,
            "error": "Website could not be reached."
        }

# ==========================================
# Check Whether NLP Signal Already Exists
# ==========================================
def nlp_signal_already_detected(category, text_lower):

    if category == "payment_request":
        payment_keywords = [
            "registration fee",
            "registration fees",
            "training fee",
            "training fees",
            "pay to apply",
            "payment required",
            "processing fee",
            "interview fee",
            "security deposit",
            "registration charge",
            "joining fee",
            "admission fee",
            "application fee",
            "activation fee"
        ]

        return any(
            has_non_negated(text_lower, keyword)
            for keyword in payment_keywords
        )

    if category == "urgency":
        urgency_keywords = [
            "urgent",
            "immediately",
            "limited seats",
            "limited time",
            "apply within",
            "act now",
            "last chance",
            "offer expires"
        ]

        return any(
            keyword in text_lower
            for keyword in urgency_keywords
        )

    if category == "guaranteed_job":
        guaranteed_rule_keywords = [
            "guaranteed job",
            "guaranteed placement"
        ]

        return any(
            keyword in text_lower
            for keyword in guaranteed_rule_keywords
        )

    if category == "off_platform_contact":
        contact_keywords = [
            "whatsapp",
            "telegram"
        ]

        return any(
            keyword in text_lower
            for keyword in contact_keywords
        )

    return False

# ==========================================
# Detect Whether Text Looks Like a Job
# ==========================================
def detect_job_posting(text):
    text_lower = text.lower()

    job_matches = []
    non_job_matches = []

    for keyword in JOB_KEYWORDS:
        if keyword in text_lower:
            job_matches.append(keyword)

    for keyword in NON_JOB_KEYWORDS:
        if keyword in text_lower:
            non_job_matches.append(keyword)

    strong_job_indicators = [
        "job description",
        "apply now",
        "job title",
        "responsibilities",
        "qualifications",
        "internship",
        "salary",
        "stipend",
        "vacancy",
        "hiring"
    ]

    strong_matches = [
        keyword
        for keyword in strong_job_indicators
        if keyword in text_lower
    ]

    if len(strong_matches) >= 1:
        return {
            "is_job_posting": True,
            "confidence": "HIGH",
            "job_keywords": job_matches,
            "non_job_keywords": non_job_matches,
            "explanation": (
                "The webpage contains indicators of "
                "a job or internship posting."
            )
        }

    if len(job_matches) >= 3 and len(non_job_matches) == 0:
        return {
            "is_job_posting": True,
            "confidence": "MEDIUM",
            "job_keywords": job_matches,
            "non_job_keywords": non_job_matches,
            "explanation": (
                "The webpage contains multiple "
                "employment-related indicators."
            )
        }

    if len(non_job_matches) >= 1 and len(job_matches) < 3:
        return {
            "is_job_posting": False,
            "confidence": "HIGH",
            "job_keywords": job_matches,
            "non_job_keywords": non_job_matches,
            "explanation": (
                "The webpage appears to be a general "
                "article, news, press release, or "
                "company information page rather "
                "than a job posting."
            )
        }

    return {
        "is_job_posting": False,
        "confidence": "LOW",
        "job_keywords": job_matches,
        "non_job_keywords": non_job_matches,
        "explanation": (
            "The webpage does not contain enough "
            "information to confidently identify "
            "it as a job or internship posting."
        )
    }

# ==========================================
# Verification Intelligence
# ==========================================
def analyze_verification_signals(text):
    text_lower = text.lower()

    verification_flags = []
    verification_points = 0

    # --------------------------------------
    # 1. Shortened URL
    # --------------------------------------
    shortened_domains = [
        "lnkd.in",
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "cutt.ly",
        "shorturl.at",
        "rb.gy"
    ]

    urls = extract_urls(text)

    for url in urls:
        try:
            domain = urlparse(
                url.rstrip(".,)")
            ).netloc.lower()

            if domain.startswith("www."):
                domain = domain[4:]

            if domain in shortened_domains:
                verification_points += 5
                verification_flags.append({
                    "flag": "Shortened application URL detected",
                    "points": 5,
                    "reason": (
                        "Shortened links can hide the final destination. "
                        "Verify the destination before applying."
                    )
                })
                break
        except Exception:
            pass

    # --------------------------------------
    # 2. Social Media Engagement
    # --------------------------------------
    engagement_patterns = [
        "comment interested",
        'comment "interested"',
        "comment interested below",
        "comment below for the link",
        "check the first comment",
        "check first comment",
        "link in the first comment",
        "application link in the comments"
    ]

    for pattern in engagement_patterns:
        if pattern in text_lower:
            verification_points += 5
            verification_flags.append({
                "flag": (
                    "Application depends on social-media comments"
                ),
                "points": 5,
                "reason": (
                    "The post directs applicants to comments "
                    "or engagement instead of directly providing "
                    "an official application page."
                )
            })
            break

    # --------------------------------------
    # 3. Third-party Disclaimer
    # --------------------------------------
    disclaimer_patterns = [
        "not associated with",
        "not affiliated with",
        "not endorsed by",
        "not officially associated",
        "not officially affiliated",
        "shared for informational purposes only"
    ]

    disclaimer_found = False

    for pattern in disclaimer_patterns:
        if pattern in text_lower:
            disclaimer_found = True
            break

    if disclaimer_found:
        verification_points += 10
        verification_flags.append({
            "flag": "Third-party affiliation disclaimer detected",
            "points": 10,
            "reason": (
                "The post states that the publisher is not officially "
                "associated with or endorsed by the mentioned company."
            )
        })

    # --------------------------------------
    # 4. Company + Non-official Application URL
    # --------------------------------------
    company_verification = verify_company(text)

    if company_verification["company_name"] and urls:
        official_company_url_found = False

        company_name = (
            company_verification["company_name"]
            .lower()
            .replace(" ", "")
        )

        for url in urls:
            try:
                domain = urlparse(
                    url.rstrip(".,)")
                ).netloc.lower()

                if domain.startswith("www."):
                    domain = domain[4:]

                domain_parts = domain.split(".")

                if len(domain_parts) >= 2:
                    domain_name = domain_parts[-2]
                else:
                    domain_name = domain

                if (
                    company_name in domain_name
                    or domain_name in company_name
                ):
                    official_company_url_found = True
                    break
            except Exception:
                pass

        if not official_company_url_found:
            verification_points += 5
            verification_flags.append({
                "flag": (
                    "Application link is not clearly an official company domain"
                ),
                "points": 5,
                "reason": (
                    "The opportunity mentions a company, but the provided "
                    "application link does not clearly belong to that company."
                )
            })

    # --------------------------------------
    # 5. No Recruiter Email
    # --------------------------------------
    emails = extract_emails(text)

    if (
        company_verification["company_name"]
        and len(emails) == 0
    ):
        verification_flags.append({
            "flag": "No recruiter or company email found",
            "points": 0,
            "reason": (
                "No recruiter email was provided, so email-domain "
                "verification could not be performed."
            )
        })

    return {
        "verification_points": verification_points,
        "verification_flags": verification_flags
    }

# ==========================================
# Main Job Analysis
# ==========================================
def analyze_job(text: str):
    text_lower = text.lower()

    risk_score = 0
    detected_flags = []

    # ======================================
    # 1. Job Posting Detection
    # ======================================
    job_detection = detect_job_posting(text)

    # ======================================
    # 2. Rule-Based Detection
    # ======================================
    for keyword, points in RED_FLAGS.items():
        if keyword in NEGATABLE_FLAGS:
            found = has_non_negated(text_lower, keyword)
        else:
            found = keyword in text_lower

        if found:
            risk_score += points
            detected_flags.append({
                "flag": keyword,
                "points": points,
                "source": "Rule-Based"
            })

    # ======================================
    # 3. NLP Analysis
    # ======================================
    nlp_result = analyze_with_nlp(text)

    for pattern in nlp_result["suspicious_patterns"]:
        category = pattern["category"]

        if nlp_signal_already_detected(
            category,
            text_lower
        ):
            continue

        risk_score += pattern["points"]
        detected_flags.append({
            "flag": pattern["message"],
            "points": pattern["points"],
            "source": "NLP"
        })

    # ======================================
    # 4. Email Analysis
    # ======================================
    emails = extract_emails(text)
    email_analysis = analyze_emails(emails)

    for email_info in email_analysis:
        if email_info["status"] == "SUSPICIOUS":
            risk_score += 10
            detected_flags.append({
                "flag": (
                    f"Free email domain: "
                    f"{email_info['domain']}"
                ),
                "points": 10,
                "source": "Email Analysis"
            })

    # ======================================
    # 5. Company Verification
    # ======================================
    company_verification = verify_company(
        text,
        emails
    )

    # ======================================
    # 6. URL Analysis
    # ======================================
    urls = extract_urls(text)
    url_analysis = []

    for url in urls:
        clean_url = url.rstrip(".,)")

        website_result = verify_website(
            clean_url
        )

        url_analysis.append(
            website_result
        )

        if not website_result["reachable"]:
            risk_score += 10
            detected_flags.append({
                "flag": "Website could not be verified",
                "points": 10,
                "source": "Website Verification"
            })

    # ======================================
    # 7. Verification Intelligence
    # ======================================
    verification_analysis = analyze_verification_signals(
        text
    )

    verification_points = (
        verification_analysis["verification_points"]
    )

    risk_score += verification_points

    for flag in verification_analysis["verification_flags"]:
        detected_flags.append({
            "flag": flag["flag"],
            "points": flag["points"],
            "source": "Verification Intelligence"
        })

    # ======================================
    # 8. Limit Risk Score
    # ======================================
    risk_score = min(
        risk_score,
        100
    )

    # ======================================
    # 9. Risk Classification
    # ======================================
    if risk_score >= 61:
        risk_level = "HIGH RISK"
        recommendation = (
            "Do not pay money or share "
            "sensitive information."
        )

    elif (
        risk_score >= 31
        or verification_points >= 15
    ):
        risk_level = "NEEDS VERIFICATION"
        recommendation = (
            "Verify the company, application link, "
            "and recruiter before proceeding."
        )

    else:
        risk_level = "LIKELY GENUINE"
        recommendation = (
            "No major scam indicators detected, "
            "but verify independently."
        )

    # ======================================
    # 10. Non-job Page Handling
    # ======================================
    if not job_detection["is_job_posting"]:
        risk_level = "NOT A JOB POSTING"
        recommendation = (
            "This URL does not appear to contain "
            "a job or internship opportunity. "
            "Verify that you are analyzing an "
            "actual job posting."
        )

    # ======================================
    # 11. Final Result
    # ======================================
    return {
        "risk_score": risk_score,
        "risk_level": risk_level,
        "red_flags": detected_flags,
        "emails": email_analysis,
        "urls": url_analysis,
        "nlp_analysis": nlp_result,
        "company_verification": company_verification,
        "job_detection": job_detection,
        "verification_analysis": verification_analysis,
        "recommendation": recommendation
    }