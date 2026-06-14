import sys
import os
# הוספת התיקייה הנוכחית לנתיב של פייתון באופן אוטומטי
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_cors import CORS

# עכשיו אנחנו מייבאים ישירות, בלי להסתבך עם 'backend.'
from routes.stocks import stocks_bp
from routes.stocks_update import update_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(stocks_bp)
app.register_blueprint(update_bp)

if __name__ == '__main__':
    app.run(debug=True)