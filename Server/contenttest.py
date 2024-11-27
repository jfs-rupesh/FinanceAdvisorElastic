import requests
import json
from sentence_transformers import SentenceTransformer

# API Configuration
API_KEY = "7PBBXVAEZCFGXS9I"
BASE_URL = "https://www.alphavantage.co/query"
COMPANY_SYMBOLS = ["TSLA", "AAPL", "MSFT", "GOOGL", "AMZN"]

# Load Pre-trained Model
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Function to fetch data from Alpha Vantage
def fetch_company_overview(symbol):
    params = {
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if "Name" in data:
            return data
    print(f"Failed to fetch data for {symbol}")
    return None

# Function to process API response into the desired JSON format
def process_data(data):
    description = data.get(
        "Description",
        "No description available."
    )
    return {
        "investment_type": "Stock",
        "name": data.get("Name"),
        "symbol": data.get("Symbol"),
        "sector": data.get("Sector", "Unknown").capitalize(),
        "industry": data.get("Industry", "Unknown").capitalize(),
        "risk_level": "High" if float(data.get("Beta", 1)) > 1.5 else "Medium",
        "timeframe": "Long-term",
        "description": description,
        "content_vector": MODEL.encode(description).tolist(),
        "market_capitalization": data.get("MarketCapitalization"),
        "pe_ratio": data.get("PERatio"),
        "price_to_book_ratio": data.get("PriceToBookRatio"),
        "analyst_target_price": data.get("AnalystTargetPrice"),
        "beta": data.get("Beta"),
        "52_week_high": data.get("52WeekHigh"),
        "52_week_low": data.get("52WeekLow"),
        "currency": data.get("Currency"),
        "exchange": data.get("Exchange")
    }

# Main Script to Generate JSON File
def generate_data():
    results = []
    for symbol in COMPANY_SYMBOLS:
        company_data = fetch_company_overview(symbol)
        if company_data:
            processed = process_data(company_data)
            results.append(processed)

    # Save to JSON
    with open("investment_data.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Data has been saved to 'investment_data.json'.")

# Run the script
if __name__ == "__main__":
    generate_data()