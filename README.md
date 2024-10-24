# SMART CALENDAR

This project automates the integration of Microsoft Teams shifts with Google Calendar, specifically designed to assist University of Florida students in managing their work schedules. It addresses the challenges of manual calendar entry and duplicate event management while ensuring compliance with work hour limits.

## Project Overview

Students faced difficulties manually adding their work shifts to calendars and calculating scheduled hours, particularly international students who must adhere to a 20-hour work limit. This solution automates these processes using Microsoft workflows and Google Calendar API.

## Challenges and Solutions

### Challenge 1: Manual Calendar Entry
- **Problem**: Lack of direct integration required manual entry of shifts.
- **Solution**: Implemented Microsoft workflows to scan user shifts for the next two weeks and send them to Google Calendar. This requires a one-time integration setup between Teams and Google Calendar.

### Challenge 2: Limited Workflow Control
- **Problem**: Workflow rules did not allow sending uniquely added calendar events.
- **Solution**: Scheduled daily updates at 6 PM to send shifts to Google Calendar.

### Challenge 3: Duplicate Calendar Events
- **Problem**: Google Calendar does not recognize duplicates if `eventId` differs, even with identical event details.
- **Solution**: Utilized Google Calendar API to identify and delete duplicate events with the same name, start time, and end time. This cleanup runs daily at 6:30 PM.

## Automation

- **Implementation**: A Flask app hosted on an EC2 instance automates this process. An AWS EventBridge function triggers the API endpoint.
- **User Interaction**: Users sign in via a hosted website for a one-time Google authentication. They can view their shift reports online.

## Additional Features

- **Slack Integration**: The workflow integrates with Slack to notify users if they exceed permitted work hours.
- **Extensibility**: The framework allows easy integration with other applications.

## Deployment Process

- **CI/CD Pipeline**: Code changes are deployed using GitHub Workflows and AWS CodePipeline. Currently, the service runs on a single EC2 instance, resulting in brief downtime during deployments.

## Getting Started

To set up this project locally or on your server, follow these steps:

1. Clone the repository.
2. Set up the necessary environment variables for Microsoft Teams and Google Calendar API integrations.
3. Deploy the Flask app on an EC2 instance or any preferred hosting service.
4. Configure AWS EventBridge to trigger the API endpoint as scheduled.
