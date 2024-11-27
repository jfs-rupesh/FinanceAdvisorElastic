import csv
import requests

API_KEY = "7PBBXVAEZCFGXS9I"
CSV_URL = f"https://www.alphavantage.co/query?function=LISTING_STATUS&apikey={API_KEY}"

# Download and parse CSV
response = requests.get(CSV_URL)
symbols = []
if response.status_code == 200:
    lines = response.text.splitlines()
    reader = csv.DictReader(lines)
    for row in reader:
        if row["status"] == "Active":  # Filter active companies
            symbols.append(row["symbol"])

print(symbols[:100])  # Display the first 100 symbols
