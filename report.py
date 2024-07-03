import datetime
import json


class ReportGenerator:
    def __init__(self, events_by_date):
        self.events_by_date = events_by_date

    def hours_between(self, start_time, end_time):
        """Calculate duration in hours between two datetime strings."""
        fmt = "%H:%M"
        start = datetime.datetime.strptime(start_time, fmt)
        end = datetime.datetime.strptime(end_time, fmt)
        duration = (end - start).seconds / 3600
        return duration

    def calculate_total_hours(self, events, event_name):
        """Calculate total hours for events with a specific name."""
        total_hours = 0
        for event in events:
            if event["summary"] == event_name:
                start_time = event["start_time"]
                end_time = event["end_time"]
                total_hours += self.hours_between(start_time, end_time)
        return total_hours

    def generate_reports(self):
        """Generate reports for events named 'AT LABS'."""
        reports = {}

        # Determine start date based on the current day of the week
        current_date = datetime.date.today()
        for i in range(4):  # Generate reports for 4 consecutive weeks

            current_weekday = current_date.weekday()
            days_until_thursday = (3 - current_weekday) % 7
            next_thursday = current_date + \
                datetime.timedelta(days=days_until_thursday)

            # Find the next Friday
            days_until_friday = (4 - current_weekday) % 7
            next_friday = current_date + \
                datetime.timedelta(days=days_until_friday)

            # Find the date of the last Friday (previous Friday)
            last_friday = next_friday - datetime.timedelta(days=7)

            # week_start = start_date
            # week_end = start_date + datetime.timedelta(days=6)  # Next Thursday

            # Find events within the current week (from today to next Thursday)
            weekly_events = []
            for date, events in self.events_by_date.items():
                event_date = datetime.datetime.strptime(
                    date, "%Y-%m-%d").date()
                if last_friday <= event_date <= next_thursday:
                    weekly_events.extend(events)

            # Calculate total hours for events named "AT LABS"
            total_hours = self.calculate_total_hours(weekly_events, "AT LABS")

            # Store the report for the current week
            # reports[f"{last_friday} - {next_thursday}"] = total_hours
            reports[f"{last_friday.strftime('%b %d')} - {next_thursday.strftime('%b %d')}"] = total_hours

            # Move to the start of the next week (next Friday)
            current_date += datetime.timedelta(days=7)

        return reports


def load_events_from_json(json_file):
    try:
        with open(json_file, "r") as file:
            events_data = json.load(file)
        return events_data
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        return {}


def fetch_report():
    # Specify the path to your events.json file
    events_json_file = "events.json"

    # Load events data from JSON file
    events_by_date = load_events_from_json(events_json_file)

    report_generator = ReportGenerator(events_by_date)
    weekly_reports = report_generator.generate_reports()

    # Prepare JSON output
    json_output = json.dumps(weekly_reports, indent=4)

    return json_output
