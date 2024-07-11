import json
from flask import Blueprint, request, jsonify
import requests
from google_calendar import GoogleCalendar
from logger import logger

# Create a Blueprint for events
events_bp = Blueprint("events", __name__)

# Initialize GoogleCalendar
calendar = GoogleCalendar()


@events_bp.route("/events", methods=["GET"])
def get_events():
    """Fetch upcoming events based on the specified number of days (default: 30 days)."""
    days = request.args.get("days", default=30, type=int)

    if days <= 0:
        logger.error("Invalid number of days")
        return jsonify({"error": "Invalid number of days"}), 400

    logger.info(f"Fetching upcoming events for {days} days")
    events_by_date = calendar.future_events(days)
    return jsonify(events_by_date)


@events_bp.route("/events", methods=["POST"])
def create_event():
    """Create a new event based on JSON payload and return the created event."""
    data = request.json
    start_datetime = data.get("start_datetime")
    end_datetime = data.get("end_datetime")
    summary = data.get("summary")

    if not start_datetime or not end_datetime or not summary:
        logger.error("Missing required fields")
        return jsonify({"error": "Missing required fields"}), 400

    logger.info("Creating a new event")
    new_event = calendar.create_event(start_datetime, end_datetime, summary)
    return jsonify(new_event)


@events_bp.route("/events/<event_id>", methods=["DELETE"])
def delete_event(event_id):
    """Delete an event by its ID and return success/failure message."""
    try:
        logger.info(f"Deleting event with ID: {event_id}")
        calendar.delete_event(event_id)
        return jsonify({"message": f"Event with ID '{event_id}' deleted successfully"})
    except Exception as e:
        logger.error(
            f"Failed to delete  event with ID: {event_id}, Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@events_bp.route("/events/delete_duplicates", methods=["POST"])
def delete_duplicate_events():
    """API route to delete duplicate events and report conflicts."""
    try:
        logger.info("Deleting duplicate events")
        num_deleted = calendar.delete_duplicate_events()
        return jsonify({"message": f"{num_deleted} duplicate events deleted successfully."}), 200
    except Exception as e:
        logger.error(f"Failed to delete duplicate events. Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@events_bp.route("/events/report", methods=["GET"])
def fetch_report():
    try:
        logger.info("Fetching report")
        report = calendar.fetch_report()
        return report, 200
    except Exception as e:
        logger.error(f"Failed to fetch report. Error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@events_bp.route("/events/forwardReports", methods=["POST"])
def forward_reports_to_slack():
    """Forward report payloads specified endpoint. """
    try:
        logger.info("Forwarding reports to Slack")
        report = calendar.fetch_report()

        # Extract JSON payload from incoming request
        data = request.json
        logger.info(f"Incoming request: {data}")

        if "workspaceName" not in data or "channelName" not in data:
            logger.error(
                "Both 'workspaceName' and 'channelName' must be provided in the request body.")
            return jsonify({"error": "Both 'workspaceName' and 'channelName' must be provided in the request body."}), 400

        workspace_name = data.get("workspaceName")
        channel_name = data.get("channelName")
        postPayload = {
            "workspaceName": workspace_name,
            "channelName": channel_name,
            "Message": "Shifts Report: "+report
        }

        # Forward the payload to the AWS API endpoint using POST request
        response = requests.post(
            "https://95lo0apboj.execute-api.us-east-1.amazonaws.com/dev", json=postPayload)

        # Check the response status code
        if response.status_code == 200:
            logger.info("Reports forwarded successfully to Slack.")
            return jsonify({"message": "Reports forwarded successfully to Slack", "response_msg": response.json()}), 200
        else:
            logger.error(
                f"Failed to forward reports to Slack. Status code: {response.status_code}, Response: {response.json()}")
            return jsonify({"error": f"Failed to forward reports to Slack. Status code: {response.status_code}", "response_msg": response.json()}), 500

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return jsonify({"error": str(e)}), 500
