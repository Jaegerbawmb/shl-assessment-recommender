import re
def normalize_space(s: str) -> str:
    return re.sub(r"\s+", " ", s or "").strip()
