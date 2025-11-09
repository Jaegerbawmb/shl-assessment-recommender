import requests
from readability import Document
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "SHL-Assignment-Reader/1.0"}

def extract_text_from_url(url: str) -> str:
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status()
    doc = Document(r.text)
    html = doc.summary()
    soup = BeautifulSoup(html, 'lxml')
    text = soup.get_text(" ", strip=True)
    return text
