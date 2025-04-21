# this one is called alert_if_cheap.py
# it for round trips from tomorrow up to 30 days out, 3-5 days in duration, and <$250. It’s Designed to be cloud-friendly and fast



import requests
from datetime import datetime, timedelta

API_KEY = 'Btd5Iuvm5amsh8puSanE83InXjpKp1O2aGzjsngu67pcw3AKy9'  # Actal KEY from SkyScanner
ORIGIN = 'LEX-sky'
DESTINATION = 'CHI-sky'
PRICE_THRESHOLD = 250
DAYS_AHEAD = 30  # Check flights within the next 30 days
MIN_STAY = 3
MAX_STAY = 5

def search_round_trip(depart_date, return_date):
    url = (
        f"https://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/US/USD/en-US/"
        f"{ORIGIN}/{DESTINATION}/{depart_date}?inboundpartialdate={return_date}&apiKey={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error fetching data for {depart_date} to {return_date}")
        return None
    return response.json()

def check_flights():
    today = datetime.today()
    for i in range(DAYS_AHEAD):
        depart_date = (today + timedelta(days=i)).strftime('%Y-%m-%d')
        for stay_length in range(MIN_STAY, MAX_STAY + 1):
            return_date = (today + timedelta(days=i + stay_length)).strftime('%Y-%m-%d')
            data = search_round_trip(depart_date, return_date)
            if not data or "Quotes" not in data:
                continue
            for quote in data["Quotes"]:
                price = quote["MinPrice"]
                if price < PRICE_THRESHOLD:
                    print(f"Flight found for ${price}! {depart_date} → {return_date}")
                    return
    print("No cheap flights found for any 3-5 day round-trip in the next 30 days.")

if __name__ == "__main__":
    check_flights()
