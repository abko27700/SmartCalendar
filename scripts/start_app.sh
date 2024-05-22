#!/bin/bash

cd /home/ec2-user/projectDaria/smartCalendar

# Install dependencies using pip
pip install flask google-auth google-auth-oauthlib google-api-python-client

# Start the application (assuming app.py with app function)
nohup gunicorn -w 2 -b 0.0.0.0:5000 app:app &