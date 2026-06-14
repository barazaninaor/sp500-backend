import pandas as pd
import requests
from bs4 import BeautifulSoup
import io

url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("--- Sending request with browser headers... ---")

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status() 
    
    print("--- Request successful! Parsing table... ---")
    
    # Use BeautifulSoup to get the table
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', {'id': 'constituents'})
    
    # Use StringIO to safely convert the table to a readable pandas dataframe
    # Using 'lxml' explicitly as the parser
    df = pd.read_html(io.StringIO(str(table)), flavor='lxml')[0]
    
    print("--- Successfully loaded the table! ---")
    
    # Force print to show only the essential info without triggering HTML rendering
    # We select only specific columns to keep the print clean
    print(df[['Symbol', 'Security', 'GICS Sector']].head().to_string())

except Exception as e:
    print(f"--- Error: {e} ---")