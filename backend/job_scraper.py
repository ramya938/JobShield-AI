import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


# --------------------------------
# Scrape job posting from URL
# --------------------------------

def scrape_job_url(url):

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        # Check HTTP status
        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary elements
        for element in soup([
            "script",
            "style",
            "noscript",
            "nav",
            "footer"
        ]):
            element.decompose()

        # Get page title
        title = ""

        if soup.title:
            title = soup.title.get_text(
                strip=True
            )

        # Extract visible text
        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Limit extremely large pages
        text = text[:20000]

        domain = urlparse(url).netloc.lower()

        return {
            "success": True,
            "url": url,
            "domain": domain,
            "title": title,
            "text": text
        }

    except requests.RequestException as error:

        return {
            "success": False,
            "url": url,
            "error": str(error)
        }

    except Exception as error:

        return {
            "success": False,
            "url": url,
            "error": f"Could not process webpage: {str(error)}"
        }