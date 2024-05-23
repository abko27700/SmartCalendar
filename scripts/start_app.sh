#!/bin/bash

cd /home/ec2-user/projectDaria/smartCalendar

sh /home/ec2-user/smartCalendarCommands.sh

# Install dependencies using pip
pip install flask google-auth google-auth-oauthlib google-api-python-client

# Start the application (assuming app.py with app function)
nohup ~/.local/bin/gunicorn -w 2 -b 0.0.0.0:5000 app:app >> /logs/smartCalendar.log 2>&1 &
