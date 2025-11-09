import json, re, time
from playwright.sync_api import sync_playwright


def extract_field(name, text):
    """Extracts a comma-separated field """
    pattern = (
        rf"{name}\s*(.*?)\s*(?:Languages|Assessment length|Test Type|Remote Testing|$)"
    )
    m = re.search(pattern, text, flags=re.IGNORECASE)
    if not m:
        return []
    parts = re.split(r"[,/]", m.group(1))
    return [p.strip() for p in parts if p.strip()]


def extract_length(text):
    """Extracts approximate completion time in minutes."""
    m = re.search(r"Approximate Completion Time in minutes\s*=\s*(\d+)", text, flags=re.IGNORECASE)
    return f"{m.group(1)} minutes" if m else None


def extract_test_types(text):
    """Extracts test types listed after 'Test Type:'"""
    m = re.search(r"Test Type:\s*([A-Z\s]+)", text)
    if not m:
        return []
    items = [t.strip() for t in m.group(1).split() if t.strip()]
    
    return list(dict.fromkeys([t for t in items if len(t) == 1]))


def clean_description(text):
    """Removes boilerplate and trims extra space."""
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"\s{2,}", " ", text)
    
    text = re.split(r"Back to Product Catalog", text, 1)[0]
    
    m = re.search(r"Description\s+(.*)", text, flags=re.IGNORECASE)
    return (m.group(1) if m else text).strip()


def fetch_details(products):
    with sync_playwright() as p:
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=True,
            args=["--no-sandbox", "--disable-gpu"]
        )
        page = browser.new_page()

        for item in products:
            url = item["url"]
            try:
                print(f"Fetching: {url}")
                page.goto(url, wait_until="domcontentloaded")
                time.sleep(2)

                text = page.inner_text("main").strip()
                desc = clean_description(text)

                item["description"] = desc[:3000]
                item["job_levels"] = extract_field("Job levels", text)
                item["languages"] = extract_field("Languages", text)
                item["assessment_length"] = extract_length(text)
                item["test_types"] = extract_test_types(text)

            except Exception as e:
                print(f"Error on {url}: {e}")
                item["description"] = ""
                item["job_levels"] = []
                item["languages"] = []
                item["assessment_length"] = None
                item["test_types"] = []
        browser.close()
    return products


if __name__ == "__main__":
    with open("data/catalog_raw.json", encoding="utf-8") as f:
        data = json.load(f)

    enriched = fetch_details(data)

    with open("data/catalog_full.json", "w", encoding="utf-8") as f:
        json.dump(enriched, f, ensure_ascii=False, indent=2)

    print("✅ Saved → data/catalog_full.json")
