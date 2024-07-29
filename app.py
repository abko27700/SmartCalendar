from flask import Flask
from flask_cors import CORS
from events import events_bp
# from auth import auth_bp
from google_calendar import GoogleCalendar

app = Flask(__name__)
app.register_blueprint(events_bp)

calendar = GoogleCalendar()
calendar.authenticate()

CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
