from flask import Blueprint, jsonify
from database import companies_collection, sectors_collection

stocks_bp = Blueprint('stocks', __name__)

# 1. GET all stocks
@stocks_bp.route('/stocks', methods=['GET'])
def get_all_stocks():
    # מיון לפי שווי שוק מהגבוה לנמוך
    stocks = list(companies_collection.find({}).sort("market_data.market_cap", -1))
    return jsonify(stocks), 200

# 2. GET all stocks with sectors
@stocks_bp.route('/stocks-with-sectors', methods=['GET'])
def get_stocks_with_sectors():
    pipeline = [
        {
            "$lookup": {
                "from": "sectors",
                "localField": "sector_id",
                "foreignField": "_id",
                "as": "sector_details"
            }
        },
        {
            "$sort": { "market_data.market_cap": -1 }
        }
    ]
    stocks = list(companies_collection.aggregate(pipeline))
    return jsonify(stocks), 200

# 3. GET all sectors
@stocks_bp.route('/sectors', methods=['GET'])
def get_all_sectors():
    sectors = list(sectors_collection.find({}))
    return jsonify(sectors), 200