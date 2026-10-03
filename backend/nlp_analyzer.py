import re
import spacy


# ==========================================
# Load spaCy English Model
# ==========================================

nlp = spacy.load("en_core_web_sm")


# ==========================================
# Suspicious Language Patterns
# ==========================================

SUSPICIOUS_PATTERNS = {

    # --------------------------------------
    # Payment / Money Requests
    # --------------------------------------

    "payment_request": {
        "patterns": [
            r"\bpay\s+(?:a\s+)?fee\b",
            r"\bpay\s+\S+\s+amount\b",
            r"\bmake\s+a\s+payment\b",
            r"\bsend\s+money\b",
            r"\bdeposit\s+\S+\s+amount\b",
            r"\bprocessing\s+fee\b",
            r"\binterview\s+fee\b",
            r"\bsecurity\s+deposit\b",
            r"\bregistration\s+charge\b",
            r"\bjoining\s+fee\b",
            r"\badmission\s+fee\b",
            r"\bapplication\s+fee\b",
            r"\bactivation\s+fee\b",
        ],
        "points": 20,
        "message": (
            "The posting appears to request money from the applicant."
        ),
    },


    # --------------------------------------
    # Urgency / Pressure
    # --------------------------------------

    "urgency": {
        "patterns": [
            r"\bact\s+now\b",
            r"\bapply\s+immediately\b",
            r"\brespond\s+immediately\b",
            r"\blimited\s+time\b",
            r"\blast\s+chance\b",
            r"\boffer\s+expires\b",
            r"\bapply\s+within\s+\d+\s+"
            r"(?:hour|hours|minute|minutes)\b",
            r"\bonly\s+\d+\s+positions?\s+left\b",
            r"\blimited\s+seats\b",
            r"\btoday\s+only\b",
        ],
        "points": 10,
        "message": (
            "The posting uses pressure or urgency to encourage quick action."
        ),
    },


    # --------------------------------------
    # Guaranteed Employment
    # --------------------------------------

    "guaranteed_job": {
        "patterns": [
            r"\bguaranteed\s+job\b",
            r"\bguaranteed\s+placement\b",
            r"\bguaranteed\s+employment\b",
            r"\bguaranteed\s+position\b",
            r"\bguaranteed\s+selection\b",
            r"\bjob\s+guaranteed\b",
            r"\bemployment\s+guaranteed\b",
            r"\bplacement\s+guaranteed\b",
            r"\b100%\s+job\b",
            r"\b100%\s+placement\b",
            r"\b100%\s+employment\b",
            r"\b100%\s+selection\b",
            r"\bassured\s+placement\b",
            r"\bassured\s+job\b",
            r"\bassured\s+employment\b",
            r"\bassured\s+selection\b",
        ],
        "points": 15,
        "message": (
            "The posting makes an unusually strong employment guarantee."
        ),
    },


    # --------------------------------------
    # Sensitive Personal Information
    # --------------------------------------

    "personal_information": {
        "patterns": [
            r"\bsend\s+your\s+aadhaar\b",
            r"\bshare\s+your\s+aadhaar\b",
            r"\bprovide\s+your\s+aadhaar\b",

            r"\bsend\s+your\s+pan\b",
            r"\bshare\s+your\s+pan\b",
            r"\bprovide\s+your\s+pan\b",

            r"\bshare\s+your\s+bank\s+details\b",
            r"\bsend\s+your\s+bank\s+details\b",
            r"\bprovide\s+your\s+bank\s+details\b",

            r"\bshare\s+your\s+bank\s+account\b",
            r"\bsend\s+your\s+bank\s+account\b",
            r"\bprovide\s+your\s+bank\s+account\b",

            r"\bsend\s+your\s+otp\b",
            r"\bshare\s+your\s+otp\b",
            r"\bprovide\s+your\s+otp\b",

            r"\bsend\s+credit\s+card\s+details\b",
            r"\bshare\s+credit\s+card\s+details\b",

            r"\bsend\s+debit\s+card\s+details\b",
            r"\bshare\s+debit\s+card\s+details\b",
        ],
        "points": 20,
        "message": (
            "The posting appears to request sensitive personal information."
        ),
    },


    # --------------------------------------
    # Off-platform Communication
    # --------------------------------------

    "off_platform_contact": {
        "patterns": [
            r"\bcontact\s+us\s+on\s+whatsapp\b",
            r"\bmessage\s+us\s+on\s+whatsapp\b",
            r"\bcontact\s+on\s+whatsapp\b",
            r"\bmessage\s+on\s+whatsapp\b",
            r"\bcontact\s+us\s+through\s+whatsapp\b",
            r"\bcontact\s+hr\s+through\s+whatsapp\b",

            r"\bcontact\s+us\s+on\s+telegram\b",
            r"\bmessage\s+us\s+on\s+telegram\b",
            r"\bcontact\s+on\s+telegram\b",
            r"\bmessage\s+on\s+telegram\b",
            r"\bcontact\s+us\s+through\s+telegram\b",
        ],
        "points": 10,
        "message": (
            "The recruiter is directing applicants to an external "
            "messaging platform."
        ),
    },


    # --------------------------------------
    # Unrealistic Salary Claims
    # --------------------------------------

    "unrealistic_salary": {
        "patterns": [
            r"\bearn\s+₹?\s*[\d,]+\s*"
            r"(?:per|a)\s+month\b",

            r"\bearn\s+\$?\s*[\d,]+\s*"
            r"(?:per|a)\s+month\b",

            r"\bearn\s+up\s+to\s+₹?\s*[\d,]+\b",

            r"\bearn\s+up\s+to\s+\$?\s*[\d,]+\b",

            r"\bsalary\s+of\s+₹?\s*[\d,]+\s*"
            r"(?:per|a)\s+month\b",

            r"\bsalary\s+of\s+\$?\s*[\d,]+\s*"
            r"(?:per|a)\s+month\b",

            r"\bno\s+experience\s+required.*₹?\s*[\d,]+",

            r"\bno\s+experience\s+required.*\$\s*[\d,]+",

            r"\beasy\s+money\b",
            r"\bquick\s+money\b",
            r"\bguaranteed\s+income\b",
            r"\bhigh\s+income\b",
        ],
        "points": 15,
        "message": (
            "The posting may contain an unusually attractive salary "
            "or income claim."
        ),
    },


    # --------------------------------------
    # Easy Income / Work From Home
    # --------------------------------------

    "easy_income": {
        "patterns": [
            r"\bno\s+experience\s+required.*high\s+salary\b",
            r"\bno\s+experience\s+required.*high\s+income\b",
            r"\bwork\s+from\s+home.*earn\b",
            r"\bwork\s+from\s+home.*income\b",
            r"\bearn\s+money\s+from\s+home\b",
            r"\bearn\s+from\s+home\s+without\s+experience\b",
        ],
        "points": 10,
        "message": (
            "The posting combines low entry requirements with "
            "attractive income claims."
        ),
    },


    # --------------------------------------
    # Threat / Intimidation Language
    # --------------------------------------

    "threat_language": {
        "patterns": [
            r"\bfailure\s+to\s+respond\b",
            r"\byour\s+application\s+will\s+be\s+cancelled\b",
            r"\bapplication\s+will\s+be\s+cancelled\b",
            r"\baccount\s+will\s+be\s+blocked\b",
            r"\bselection\s+will\s+be\s+cancelled\b",
            r"\byou\s+will\s+lose\s+the\s+opportunity\b",
            r"\bdo\s+not\s+ignore\b",
            r"\byour\s+opportunity\s+will\s+be\s+cancelled\b",
        ],
        "points": 10,
        "message": (
            "The posting uses threatening or intimidating language."
        ),
    },
}


# ==========================================
# Detect Suspicious Patterns
# ==========================================

def detect_suspicious_patterns(text):

    results = []
    total_points = 0

    text_lower = text.lower()

    for category, data in SUSPICIOUS_PATTERNS.items():

        category_detected = False

        for pattern in data["patterns"]:

            if re.search(
                pattern,
                text_lower,
                flags=re.IGNORECASE
            ):
                category_detected = True
                break

        if category_detected:

            total_points += data["points"]

            results.append({
                "category": category,
                "points": data["points"],
                "message": data["message"]
            })

    return {
        "nlp_risk_points": total_points,
        "suspicious_patterns": results
    }


# ==========================================
# Extract Entities Using spaCy
# ==========================================

def extract_entities(text):

    doc = nlp(text)

    organizations = []
    locations = []
    people = []

    # Words that should not be treated
    # as company names

    excluded_organizations = {
        "whatsapp",
        "telegram",
        "aadhaar",
        "pan",
        "linkedin",
        "instagram",
        "facebook",
        "gmail",
        "outlook",
        "yahoo",
    }

    # Common job-related phrases that spaCy
    # can incorrectly classify as organizations

    excluded_phrases = {
        "software developer internship",
        "software developer",
        "software engineering intern",
        "internship",
        "internship program",
        "job",
        "job opportunity",
        "work from home",
        "global careers india",
    }

    for entity in doc.ents:

        entity_text = entity.text.strip()
        entity_lower = entity_text.lower()

        if entity.label_ == "ORG":

            if entity_lower not in excluded_organizations:

                if entity_lower not in excluded_phrases:

                    organizations.append(entity_text)

        elif entity.label_ == "GPE":

            locations.append(entity_text)

        elif entity.label_ == "PERSON":

            people.append(entity_text)


    # Remove duplicates

    organizations = list(
        dict.fromkeys(organizations)
    )

    locations = list(
        dict.fromkeys(locations)
    )

    people = list(
        dict.fromkeys(people)
    )


    return {
        "companies": organizations,
        "organizations": organizations,
        "locations": locations,
        "people": people
    }


# ==========================================
# Complete NLP Analysis
# ==========================================

def analyze_with_nlp(text):

    suspicious = detect_suspicious_patterns(text)

    entities = extract_entities(text)

    return {
        "nlp_risk_points": suspicious["nlp_risk_points"],
        "suspicious_patterns": suspicious["suspicious_patterns"],
        "entities": entities
    }