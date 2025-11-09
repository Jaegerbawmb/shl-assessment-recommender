import json
import time
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

URL = "https://www.shl.com/products/product-catalog/"

def scrape_page(page, url):
    page.goto(url, wait_until="networkidle")
    time.sleep(3)
    cards = page.query_selector_all("a[href*='/products/product-catalog/view/']")
    data = []
    for c in cards:
        title = c.inner_text().strip()
        href = c.get_attribute("href")
        if not title or not href:
            continue
        full_url = urljoin(URL, href)
        data.append({
            "name": title,
            "url": full_url,
            "description": "",
            "test_types": []
        })
    return data

def crawl_catalog():
    print(f"Opening {URL} with local Chrome...")
    with sync_playwright() as p:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=True,
            args=["--no-sandbox", "--disable-gpu"]
        )
        page = browser.new_page()

        all_data = []
        next_page = URL
        while next_page:
            print(f"Scraping: {next_page}")
            products = scrape_page(page, next_page)
            all_data.extend(products)

            next_button = page.query_selector("a.next.page-numbers")
            if next_button:
                href = next_button.get_attribute("href")
                next_page = urljoin(URL, href)
            else:
                next_page = None

        browser.close()

    seen = set()
    unique_data = []
    for item in all_data:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique_data.append(item)

    print(f"✅ Found {len(unique_data)} unique products.")
    with open("data/catalog_raw.json", "w", encoding="utf-8") as f:
        json.dump(unique_data, f, ensure_ascii=False, indent=2)
    print("Saved → data/catalog_raw.json")

if __name__ == "__main__":
    crawl_catalog()
