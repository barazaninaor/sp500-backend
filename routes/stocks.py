from flask import Blueprint, jsonify
from database import companies_collection, sectors_collection
from bson import json_util
import json

stocks_bp = Blueprint('stocks', __name__)

# פונקציית עזר להמרה בטוחה ל-JSON
def safe_jsonify(data):
    return json.loads(json_util.dumps(data))

# 1. GET all stocks
@stocks_bp.route('/stocks', methods=['GET'])
def get_all_stocks():
    stocks = list(companies_collection.find({}).sort("market_data.market_cap", -1))
    return jsonify(safe_jsonify(stocks)), 200

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
    return jsonify(safe_jsonify(stocks)), 200

# 3. GET all sectors
@stocks_bp.route('/sectors', methods=['GET'])
def get_all_sectors():
    sectors = list(sectors_collection.find({}))
    return jsonify(safe_jsonify(sectors)), 200