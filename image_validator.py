import csv
from constants import URL_PREFIX_MAP, CSV_FILE
from url_formatter import slugify, url_exists, build_image_url

def validate_csv():
    missing = []
    total = 0

    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            name = row.get("Card Name", "").strip()
            source = row.get("Source", "").strip()
            card_type = row.get("Card Type", "").strip()
            website_name = row.get("Website Name", "").strip()

            if not name or not source or not card_type:
                continue

            total += 1
            url = build_image_url(name, website_name, source, card_type)

            if not url:
                print(f"❌ No URL prefix mapping for: {name} ({source}, {card_type})")
                missing.append((name, "NO PREFIX"))
                continue

            if url_exists(url):
                print(f"✅ {name} → OK")
            else:
                print(f"❌ {name} → MISSING IMAGE\n   {url}")
                missing.append((name, url))

    print("\n-----------------------------------")
    print(f"Checked {total} cards")
    print(f"Missing images: {len(missing)}")
    print("-----------------------------------")

    if missing:
        print("\nMissing list:")
        for name, url in missing:
            print(f"- {name}: {url}")

if __name__ == "__main__":
    validate_csv()
