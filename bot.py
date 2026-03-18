import schedule
import time

from constants import TIME_TO_POST
from functions import load_cards, load_used_cards, pick_card, send_card

def daily_task():
    cards = load_cards()
    used = load_used_cards()
    card = pick_card(cards, used)
    send_card(card)
    print(f"Sent card: {card['name']}")

schedule.every().day.at(TIME_TO_POST).do(daily_task)

print("Dune Imperium card bot running...")

while True:
    schedule.run_pending()
    time.sleep(1)
