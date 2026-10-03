import re
from urllib.parse import urlparse


SHORTENED_DOMAINS = {
    "lnkd.in",
    "bit.ly",
    "tinyurl.com",
    "t.co",
    "cutt.ly",
    "shorturl.at",
    "rb.gy",
}


# Known companies that JobShield can recognize directly.
KNOWN_COMPANIES = [
    "Cognizant",
    "TCS",
    "Infosys",
    "Accenture",
    "Wipro",
    "IBM",
    "Microsoft",
    "Google",
    "Amazon",
]


def extract_company_name(text):
    """
    Extract the most likely company name from a job posting.
    """

    # -------------------------------------------------
    # 1. Check known company names FIRST
    # -------------------------------------------------

    for company in KNOWN_COMPANIES:
        pattern = rf"\b{re.escape(company)}\b"

        if re.search(pattern, text, flags=re.IGNORECASE):
            return company

    # -------------------------------------------------
    # 2. Explicit company fields
    # -------------------------------------------------

    patterns = [
        r"company\s*:\s*([A-Za-z0-9&.,'\- ]{2,60})",
        r"company\s+name\s*:\s*([A-Za-z0-9&.,'\- ]{2,60})",
        r"organization\s*:\s*([A-Za-z0-9&.,'\- ]{2,60})",
        r"employer\s*:\s*([A-Za-z0-9&.,'\- ]{2,60})",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        if match:

            company = match.group(1).strip()

            company = re.sub(
                r"\s+(we|is|are|and|for|as|with|looking|hiring|has|have|officially)$",
                "",
                company,
                flags=re.IGNORECASE
            )

            company = company.strip(" .,:;-")

            if len(company) >= 2:
                return company

    # -------------------------------------------------
    # 3. Specific wording around company names
    # -------------------------------------------------

    patterns = [
        r"internship\s+(?:with|at|from)\s+([A-Z][A-Za-z0-9&.\- ]{2,50})",
        r"internship\s+by\s+([A-Z][A-Za-z0-9&.\- ]{2,50})",
        r"program\s+by\s+([A-Z][A-Za-z0-9&.\- ]{2,50})",
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text
        )

        if match:

            company = match.group(1).strip()

            # Stop accidental capture at common sentence words.
            company = re.split(
                r"\s+(?:is|has|will|offers|provides|for|and|that|which)\b",
                company,
                maxsplit=1,
                flags=re.IGNORECASE
            )[0]

            company = company.strip(" .,:;-")

            if len(company) >= 2:
                return company

    return None


def get_domain_from_url(url):
    """
    Extract domain from URL.
    """

    try:

        parsed = urlparse(url)

        domain = parsed.netloc.lower()

        if domain.startswith("www."):
            domain = domain[4:]

        return domain

    except Exception:

        return None


def extract_websites(text):
    """
    Extract URLs and identify shortened URLs.
    """

    urls = re.findall(
        r"https?://[^\s]+",
        text
    )

    websites = []

    for url in urls:

        clean_url = url.rstrip(".,)")

        domain = get_domain_from_url(
            clean_url
        )

        if domain:

            is_shortened = (
                domain in SHORTENED_DOMAINS
            )

            websites.append({
                "url": clean_url,
                "domain": domain,
                "is_shortened": is_shortened
            })

    return websites


def compare_email_domain(
    email,
    website_domain
):
    """
    Compare recruiter email domain
    with company website domain.
    """

    if not email or not website_domain:

        return {
            "match": False,
            "reason": (
                "Email or website domain is unavailable."
            )
        }

    email_domain = (
        email.split("@")[-1].lower()
    )

    if email_domain == website_domain:

        return {
            "match": True,
            "email_domain": email_domain,
            "website_domain": website_domain,
            "reason": (
                "Recruiter email domain matches "
                "the company website."
            )
        }

    return {
        "match": False,
        "email_domain": email_domain,
        "website_domain": website_domain,
        "reason": (
            "Recruiter email domain does not match "
            "the company website."
        )
    }


def verify_company(
    text,
    emails=None
):
    """
    Perform company and recruiter verification.
    """

    # -------------------------------------------------
    # Company name
    # -------------------------------------------------

    company_name = extract_company_name(
        text
    )

    # -------------------------------------------------
    # URLs
    # -------------------------------------------------

    all_websites = extract_websites(
        text
    )

    # Ignore shortened URLs when identifying
    # an actual company website.
    company_websites = [
        website
        for website in all_websites
        if not website["is_shortened"]
    ]

    website_domain = None

    if company_websites:

        website_domain = (
            company_websites[0]["domain"]
        )

    # -------------------------------------------------
    # Email verification
    # -------------------------------------------------

    email_checks = []

    if emails and website_domain:

        for email in emails:

            email_checks.append(
                compare_email_domain(
                    email,
                    website_domain
                )
            )

    # -------------------------------------------------
    # Verification logic
    # -------------------------------------------------

    website_available = (
        len(company_websites) > 0
    )

    matching_email = any(
        check["match"]
        for check in email_checks
    )

    # -------------------------------------------------
    # Strong verification
    # -------------------------------------------------

    if website_available and matching_email:

        verification_status = "STRONG"

        explanation = (
            "A company website was found and "
            "the recruiter email domain matches "
            "the website domain."
        )

    # -------------------------------------------------
    # Website + mismatching email
    # -------------------------------------------------

    elif website_available and email_checks:

        verification_status = (
            "NEEDS VERIFICATION"
        )

        explanation = (
            "A company website was found, but "
            "the recruiter email domain does not "
            "match the website domain."
        )

    # -------------------------------------------------
    # Website but no recruiter email
    # -------------------------------------------------

    elif website_available:

        verification_status = (
            "NEEDS VERIFICATION"
        )

        explanation = (
            "A company website was found, but "
            "no recruiter email could be confirmed "
            "against the website domain."
        )

    # -------------------------------------------------
    # Company found but no official website
    # -------------------------------------------------

    elif company_name:

        verification_status = (
            "NEEDS VERIFICATION"
        )

        if all_websites:

            explanation = (
                f"The posting mentions '{company_name}', "
                "but the provided link is not a direct "
                "company website. The company could not "
                "be independently verified."
            )

        else:

            explanation = (
                f"The posting identifies the company "
                f"as '{company_name}', but no company "
                "website was provided for verification."
            )

    # -------------------------------------------------
    # No company information
    # -------------------------------------------------

    else:

        verification_status = "UNKNOWN"

        explanation = (
            "The posting does not provide enough "
            "company information for verification."
        )

    return {
        "company_name": company_name,
        "websites": all_websites,
        "company_websites": company_websites,
        "email_checks": email_checks,
        "verification_status": verification_status,
        "explanation": explanation
    }