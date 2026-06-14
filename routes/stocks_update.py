import sys
import os
# מוסיף את התיקייה של ה-backend לנתיב כדי שיימצא את ה-utils
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from flask import Blueprint, jsonify
import datetime
import time
# כאן השינוי: וודא שהנתיב לתיקיית utils נכון מהמיקום של הקובץ הנוכחי
from utils.scraper import update_sp500_data 

update_bp = Blueprint('update_bp', __name__)
update_tracker = {"count": 0, "last_reset": datetime.date.today()}

@update_bp.route('/admin/update-data', methods=['POST'])
def trigger_update():
    global update_tracker
    today = datetime.date.today()

    if update_tracker["last_reset"] != today:
        update_tracker = {"count": 0, "last_reset": today}

    if update_tracker["count"] >= 3:
        return jsonify({"error": "Update limit reached (3/24h)"}), 429

    try:
        start = time.time()
        # הרצת הפונקציה מה-utils
        update_sp500_data()
        duration = time.time() - start
        
        update_tracker["count"] += 1
        
        return jsonify({
            "message": f"Update completed in {duration:.2f} seconds!",
            "remaining": 3 - update_tracker["count"]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500