import requests
from bs4 import BeautifulSoup
from typing import List
import re

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

def fetch_html(url: str) -> str:
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=15
        )
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return ""

    
def remove_irrelevant_tags(soup: BeautifulSoup) -> None:
    """
    Removes headers, footers, navbars, scripts, styles, ads.
    """
    for tag in soup([
        "header", "footer", "nav", "aside",
        "script", "style", "noscript", "iframe"
    ]):
        tag.decompose()
        
def extract_text(soup: BeautifulSoup):
    texts = []

    article_div = soup.find("div", {"data-testid": "post-content"})
    if article_div:
        for p in article_div.find_all("p"):
            text = p.get_text(strip=True)
            if len(text.split()) > 5:
                texts.append(text)

    if texts:
        return texts

    # fallback for normal websites
    for element in soup.find_all(["p", "h1", "h2", "h3", "article", "div", "section"]):
        text = element.get_text(strip=True)
        if len(text.split()) > 5:
            texts.append(text)

    return texts

def remove_duplicates(text_blocks: List[str]) -> List[str]:
    """
    Remove duplicate or near-duplicate text blocks.
    """
    seen = set()
    unique_texts = []

    for text in text_blocks:
        normalized = re.sub(r"\s+", " ", text.lower())
        if normalized not in seen:
            seen.add(normalized)
            unique_texts.append(text)

    return unique_texts


def normalize_url(url: str) -> str:
    """
    Convert JS-heavy URLs (like Medium) to readable text versions.
    """
    if "medium.com" in url:
        return f"https://r.jina.ai/http://{url.replace('https://', '').replace('http://', '')}"
    return url


from bs4 import BeautifulSoup

import requests
from bs4 import BeautifulSoup

session = requests.Session()

def crawl_website(url: str) -> str:
    try:
        response = session.get(
            url,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=(5, 30)  # connect timeout, read timeout
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text(separator="\n", strip=True)

    except requests.exceptions.RequestException as e:
        print("CRAWL ERROR:", e)
        return ""



#print(crawl_website("https://openrouter.ai/openai/gpt-oss-120b:free"))  # Example usage