import sys
import os

# מוסיף את תיקיית ה-root לנתיב של פייתון
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
# ייבוא מה-Blueprints שלך
from routes.stocks import stocks_bp
from routes.stocks_update import update_bp

app = Flask(__name__)

# הגדרת CORS - מאפשר גישה מכל מקור, או הגדר דומיין ספציפי ליתר ביטחון
CORS(app, resources={r"/*": {"origins": "*"}})

# רישום ה-Blueprints
app.register_blueprint(stocks_bp)
app.register_blueprint(update_bp)

# נתיב בדיקה לראות שהשרת חי (מונע 404 בדף הבית)
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "S&P 500 Backend is running!", "status": "online"})

# טיפול גלובלי בשגיאות 404
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    # ב-Render/Gunicorn זה לא ירוץ, זה רק למחשב האישי שלך
    app.run(debug=True, port=5000)
