from discord_webhook import DiscordWebhook, DiscordEmbed
import csv
import json
import random
import os
from dotenv import load_dotenv

from constants import CSV_FILE, USED_CARDS_FILE
from url_formatter import build_image_url, url_exists, slugify

load_dotenv()
webhookUrl = os.environ.get("DISCORD_WEBHOOK_URL")
if not webhookUrl:
    raise ValueError("DISCORD_WEBHOOK_URL is missing or not loaded from .env")

def load_cards():
    cards = []
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("Card Name", "").strip()
            source = row.get("Source", "").strip()
            card_type = row.get("Card Type", "").strip()
            website_name = row.get("Website Name", "").strip()

            if not name or not source or not card_type:
                continue

            cards.append({
                "name": name,
                "source": source,
                "card_type": card_type,
                "website_name": website_name
            })
    return cards

def load_used_cards():
    if not os.path.exists(USED_CARDS_FILE):
        return []
    with open(USED_CARDS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_used_cards(used):
    with open(USED_CARDS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, indent=2)

def pick_card(cards, used):
    unused = [c for c in cards if c["name"] not in used]

    if not unused:
        used.clear()
        unused = cards

    card = random.choice(unused)
    used.append(card["name"])
    save_used_cards(used)
    return card

def send_card(card):
    image_url = build_image_url(
        card["name"],
        card["website_name"],
        card["source"],
        card["card_type"]
    )

    image_found = url_exists(image_url) if image_url else False

    webhook = DiscordWebhook(url=str(webhookUrl))

    description = ""
    if not image_found:
        description = "**Image not found for this card**"

    embed = DiscordEmbed(
        title=card["name"],
        description=description,
        color=0x3498db
    )

    embed.add_embed_field(name="Card Name", value=card["name"], inline=False)
    embed.add_embed_field(name="Source", value=card["source"], inline=True)
    embed.add_embed_field(name="Card Type", value=card["card_type"], inline=True)

    if image_found and image_url:
        embed.set_image(url=image_url)

    webhook.add_embed(embed)
    webhook.execute()

    if not image_found:
        print(f"WARNING: Image not found → {image_url}")