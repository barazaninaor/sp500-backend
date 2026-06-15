import sys
import os
import io
import requests
import pandas as pd
import yfinance as yf
from bs4 import BeautifulSoup
import time
import gc

# Fix path to import database (if running from subfolder)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database import companies_collection, sectors_collection

def update_sp500_data():
    print("Starting optimized data scrape...")
    
    # 1. Wikipedia: Fetch and Parse
    url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'id': 'constituents'})
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
    symbols = [entry['Symbol'] for entry in data]
    
    # 2. Update Sectors
    for entry in data:
        sector_name = entry['Sector']
        sector_id = sector_name.lower().replace(" ", "_")
        sectors_collection.update_one(
            {"_id": sector_id},
            {"$set": {"name": sector_name}},
            upsert=True
        )

    # 3. Yahoo Finance: Get dynamic market data with strict memory limits
    # הקטנה ל-10 מניות ב-Batch כדי למנוע Memory Overflow ב-Render
    batch_size = 10 
    for i in range(0, len(symbols), batch_size):
        batch = symbols[i : i + batch_size]
        print(f"Processing batch {i//batch_size + 1}: {batch}")
        
        try:
            # threads=False מונע יצירת תהליכי משנה כבדים שגורמים ל-SIGKILL בשרת חינמי
            batch_data = yf.download(batch, period="1d", group_by='ticker', progress=False, threads=False)
            
            for entry in data:
                symbol = entry['Symbol']
                if symbol in batch:
                    try:
                        # טיפול במבנה נתונים שונה בהתאם לכמות התוצאות
                        stock_info = batch_data[symbol] if len(batch) > 1 else batch_data
                        
                        last_price = float(stock_info['Close'].iloc[-1])
                        prev_close = float(stock_info['Open'].iloc[0]) 
                        
                        company_doc = {
                            "_id": symbol,
                            "name": entry['Security'],
                            "sector_id": entry['Sector'].lower().replace(" ", "_"),
                            "details": {
                                "sub_industry": entry['Sub_Industry'],
                                "headquarters": entry['Headquarters'],
                                "founded": entry['Founded']
                            },
                            "market_data": {
                                "last_price": round(last_price, 2),
                                "change": round(last_price - prev_close, 2),
                                "percent_change": round(((last_price - prev_close) / prev_close) * 100, 2),
                                "volume": int(stock_info['Volume'].iloc[-1])
                            }
                        }
                        companies_collection.update_one({"_id": symbol}, {"$set": company_doc}, upsert=True)
                    except Exception as e:
                        print(f"Error updating {symbol}: {e}")
        
        except Exception as e:
            print(f"Batch processing error: {e}")
        
        # ניקוי זיכרון אגרסיבי והשהיה
        del batch_data
        gc.collect()
        time.sleep(4) 

    print("Full scraping process completed successfully!")

if __name__ == "__main__":
    update_sp500_data()