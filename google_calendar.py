import datetime
from http.server import BaseHTTPRequestHandler
import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import json
import events
import report
from googleapiclient.http import BatchHttpRequest

SCOPES = ["https://www.googleapis.com/auth/calendar"]

class GoogleCalendar:
    def __init__(self):
        self.scopes = SCOPES
        self.creds = self.authenticate()
        self.service = build("calendar", "v3", credentials=self.creds)

    def authenticate(self):
        """Authenticate using OAuth 2.0 and return the credentials."""
        creds = None

        # Load credentials from token.json if it exists
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", self.scopes)

        # If there are no (valid) credentials available, initiate OAuth 2.0 flow
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", self.scopes
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials to token.json for future use
            with open("token.json", "w") as token:
                token.write(creds.to_json())

        return creds

    def future_events(self, days):
        output_file="events.json"
        if not self.service:
            return {}  # 
        """Fetch upcoming events for the specified number of days and organize them by date."""
        now = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        end_date = now + datetime.timedelta(days=days)
        time_min = now.isoformat() + "Z"
        time_max = end_date.isoformat() + "Z"

        events_result = (
            self.service.events()
            .list(
                calendarId="primary",
                timeMin=time_min,
                timeMax=time_max,
                maxResults=200,  # Adjust maxResults as needed
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])

        events_by_date = {}
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            end = event["end"].get("dateTime", event["end"].get("date"))
            summary = event["summary"]
            event_id = event["id"]

            event_data = {
                "event_id": event_id,
                "start_time": start.split("T")[1][:5],
                "end_time": end.split("T")[1][:5],
                "summary": summary,
            }

            event_date = start.split("T")[0]
            if event_date not in events_by_date:
                events_by_date[event_date] = []

            events_by_date[event_date].append(event_data)
        
        print("Returning data")

        #to make sure the json is empty, then we write new data.
        with open(output_file, "w") as json_file:
            json.dump({}, json_file)

        with open(output_file, "w") as json_file:
            json.dump(events_by_date, json_file, indent=4)

        return events_by_date

    def create_event(self, start_datetime, end_datetime, summary, calendar_id="primary"):
        """Create a new event on the calendar."""
        event = {
            "summary": summary,
            "start": {"dateTime": start_datetime},
            "end": {"dateTime": end_datetime},
        }

        created_event = (
            self.service.events()
            .insert(calendarId=calendar_id, body=event)
            .execute()
        )

        return created_event

    def delete_event(self, event_id, calendar_id="primary"):
        """Delete an event from the calendar given its event ID."""
        try:
            self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
            return True
        except Exception as e:
            print(f"An error occurred while deleting the event: {e}")
            return False

    def delete_duplicate_events(self,calendar_id="primary"):
        """Delete duplicate events"""
        events_by_date=self.future_events(30)
        print("fetched calendar events!")
        num_deleted = 0
        duplicate_list=[]
        for date, event_list in events_by_date.items():
            events_map = {}
            for event in event_list:
                # print("inside list")
                start_time = event["start_time"]
                end_time = event["end_time"]
                summary = event["summary"]
                event_id = event["event_id"]

                # Generate a unique key based on start time, end time, and summary
                event_key = f"{start_time}-{end_time}-{summary}"

                # Check if event_key already exists in events_map
                if event_key in events_map:
                    self.service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
                    num_deleted+=1
                else:
                    # Add event to events_map with its unique key
                    events_map[event_key] = True
        # self.batch_delete(duplicate_list,calendar_id)
                    
        self.future_events(30)
                
        return num_deleted  # Operation completed successfully
    
    def fetch_report(self,calendar_id="primary"):
        self.delete_duplicate_events()
        return report.fetch_report()
    

    def batch_delete(self,events,calendar_id="primary"):
        for event in events:
            try:
                self.service.events().delete(calendarId=calendar_id, eventId=event).execute()
                return True
            except Exception as e:
                print(f"An error occurred while deleting the event: {e}")
                return False