#!/bin/bash

sudo pkill -f gunicorn
cd /home/ec2-user/projectDaria/smartCalendar

cp /home/ec2-user/secrets/* /home/ec2-user/projectDaria/smartCalendar/

touch /home/ec2-user/projectDaria/smartCalendar/logs/deployment.log
touch /home/ec2-user/projectDaria/smartCalendar/logs/smartCalendar.log

# Install dependencies using pip .
pip install flask flask-cors google-auth google-auth-oauthlib google-api-python-client gunicorn


# Start the application (assuming app.py with app function) 
nohup gunicorn -w 2 -b 0.0.0.0:5000 app:app >> /home/ec2-user/projectDaria/smartCalendar/logs/smartCalendar.log 2>&1 &

echo "Code Deployed" >> /home/ec2-user/projectDaria/smartCalendar/logs/deployment.log
