from flask import Flask
from events import events_bp
# from auth import auth_bp
from google_calendar import GoogleCalendar

app = Flask(__name__)
app.register_blueprint(events_bp)
# app.register_blueprint(auth_bp)

calendar = GoogleCalendar()
calendar.authenticate()

if __name__ == "__main__":
    app.run(debug=True)
