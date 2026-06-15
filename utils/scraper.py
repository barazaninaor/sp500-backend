import sys
import os
import io
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup

# Fix path to import database (preventing circular import)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import companies_collection, sectors_collection

def update_sp500_data():
    print("Starting full data scrape (Wikipedia + Yahoo)...")
    
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    # 1. Wikipedia: Fetch and Parse
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'constituents'})
        
        # Use StringIO and lxml to ensure clean table parsing
        df = pd.read_html(io.StringIO(str(table)), flavor='lxml')[0]
        
        df = df.rename(columns={
            'GICS Sector': 'Sector', 
            'GICS Sub-Industry': 'Sub_Industry', 
            'Headquarters Location': 'Headquarters'
        })
    except Exception as e:
        print(f"Failed to scrape Wikipedia: {e}")
        return

    data = df.to_dict('records')
    
    # 2. Update Database
    for entry in data:
        symbol = entry['Symbol']
        sector_name = entry['Sector']
        sector_id = sector_name.lower().replace(" ", "_")
        
        # Save or update the sector
        sectors_collection.update_one(
            {"_id": sector_id},
            {"$set": {"name": sector_name}},
            upsert=True
        )
        
        # 3. Yahoo Finance: Get dynamic market data
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            
            company_doc = {
                "_id": symbol,
                "name": entry['Security'],
                "sector_id": sector_id,
                "details": {
                    "sub_industry": entry['Sub_Industry'],
                    "headquarters": entry['Headquarters'],
                    "founded": entry['Founded']
                },
                "market_data": {
                    "last_price": round(info.last_price, 2),
                    "change": round(info.last_price - info.previous_close, 2),
                    "percent_change": round(((info.last_price - info.previous_close) / info.previous_close) * 100, 2),
                    "volume": info.last_volume,
                    "market_cap": info.market_cap
                }
            }
            
            companies_collection.update_one({"_id": symbol}, {"$set": company_doc}, upsert=True)
            print(f"Successfully updated {symbol}")
            
        except Exception as e:
            print(f"Error updating {symbol}: {e}")

    print("Full scraping process completed!")

if __name__ == "__main__":
    update_sp500_data()
