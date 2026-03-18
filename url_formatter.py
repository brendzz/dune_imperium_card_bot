import re
import requests
from constants import URL_PREFIX_MAP, WEBSITE_URL, IMAGE_FORMAT

def slugify(name):
    name = name.lower().strip()
    name = name.replace("’", "'")
    name = name.replace("'", "-")
    name = re.sub(r"[^a-z0-9\- ]", "", name)
    name = name.replace(" ", "-")
    name = re.sub(r"-+", "-", name)   
    return name

def url_exists(url):
    try:
        r = requests.head(url, timeout=5)
        return r.status_code == 200
    except requests.RequestException:
        return False

def build_image_url(card_name, website_name, source, card_type):
    key = (source, card_type)
    if key not in URL_PREFIX_MAP:
        return None

    prefix = URL_PREFIX_MAP[key]

    # Some cards have typos, hence use Website Name if provided, otherwise Card Name
    name_for_url = website_name if website_name else card_name
    card_slug = slugify(name_for_url)

    return f"{WEBSITE_URL}{prefix}-{card_slug}{IMAGE_FORMAT}"
