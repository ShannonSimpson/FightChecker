import time
import requests

API_KEY = 'your_skyscanner_api_key'  # Replace with your actual API key
ORIGIN = 'LEX-sky'  # Lexington, KY
DESTINATION = 'CHI-sky'  # Chicago, IL (all airports)
PRICE_THRESHOLD = 250
CHECK_INTERVAL = 86400  # Check once every 24 hours

def check_flights():
   url = 'https://partners.api.skyscanner.net/apiservices/browseroutes/v1.0/US/USD/en-US/{}/{}/2025-05-01?apiKey={}'.format(
       ORIGIN, DESTINATION, API_KEY
   )
   response = requests.get(url)
   data = response.json()

   for quote in data.get('Quotes', []):
       price = quote['MinPrice']
       if price < PRICE_THRESHOLD:
           print(f"Flight found for ${price}!")
           # Add alert (email, text, etc.)
           return
   print("No cheap flights found today.")

while True:
   check_flights()
   time.sleep(CHECK_INTERVAL)