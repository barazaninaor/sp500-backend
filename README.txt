Project: StockAI - REST API Web Server
======================================

Description:
This project is a RESTful web server built with Flask and MongoDB. 
It provides a platform to explore stock market data, including company 
details and sector classifications.

Project Structure:
- app.py: The entry point of the application.
- database.py: Handles the connection to the MongoDB Atlas database.
- routes/stocks.py: Contains all API endpoints and aggregation logic.
- utils/: Contains the scraper logic to populate the database.
- models/: Data structure definitions.

Fulfillment of Project Requirements:

1. Server Technology: 
   - Built using Flask (Python).

2. Database (MongoDB): 
   - Used MongoDB Atlas with two main collections: 'companies' and 'sectors'.

3. Data Modeling:
   - Embedded Document: Each company document contains 'details' and 
     'market_data' as embedded objects to optimize read performance.
   - Referenced Document: Each company document contains a 'sector_id', 
     linking it to a separate 'sectors' collection for data normalization.

4. REST API Requirements:
   - GET all main documents (stocks only): 
     Endpoint: GET /stocks
     Description: Returns the full list of companies without joining external data.
     http://127.0.0.1:5000/stocks
   
   - GET all main documents (stocks + full sector details):
     Endpoint: GET /stocks-with-sectors
     Description: Uses MongoDB '$lookup' aggregation to perform a LEFT OUTER JOIN 
     between the companies and sectors collections.
     http://127.0.0.1:5000/stocks-with-sectors
   
   - GET referenced resource only (sectors):
     Endpoint: GET /sectors
     Description: Returns the full list of sectors from the sectors collection.
     http://127.0.0.1:5000/sectors

How to Run:
1. Ensure Python 3.x is installed.
2. Create and activate a virtual environment.
3. Install requirements: pip install flask pymongo yfinance
4. Run the server: python app.py
5. Access the API at http://127.0.0.1:5000/