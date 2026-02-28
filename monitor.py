import requests
import json
import smtplib
import os

API_KEY = os.environ["TM_API_KEY"]
EMAIL_USER = os.environ["EMAIL_USER"]
EMAIL_PASS = os.environ["EMAIL_PASS"]
EMAIL_TO = os.environ["EMAIL_TO"]

KEYWORD = "Las Vegas Grand Prix 2026"

def get_prices():
    url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "keyword": KEYWORD,
        "countryCode": "US"
    }

    r = requests.get(url, params=params)
    data = r.json()

    prices = []

    if "_embedded" in data:
        for event in data["_embedded"]["events"]:
            if "priceRanges" in event:
                for p in event["priceRanges"]:
                    prices.append({
                        "min": p["min"],
                        "max": p["max"],
                        "currency": p["currency"]
                    })

    return prices


def send_email(message):
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(
            EMAIL_USER,
            EMAIL_TO,
            f"Subject: F1 Ticket Price Update\n\n{message}"
        )


def main():
    new_prices = get_prices()

    try:
        with open("prices.json") as f:
            old_prices = json.load(f)
    except:
        old_prices = []

    if new_prices != old_prices:
        send_email(f"New prices:\n{json.dumps(new_prices, indent=2)}")
        with open("prices.json", "w") as f:
            json.dump(new_prices, f)


if __name__ == "__main__":
    main()
