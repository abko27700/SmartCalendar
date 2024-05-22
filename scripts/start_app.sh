#!/bin/bash

# Change to the project directory
cd /home/ec2-user/projectDaria/smartCalendar

# Install Pipenv if not already installed
python3 -m ensurepip --upgrade
python3 -m pip install --user pipenv

# Add Pipenv to the PATH
export PATH="/home/ec2-user/.local/bin:$PATH"

# Install project dependencies using Pipenv
pipenv install --deploy

# Start the application using Gunicorn
pipenv run nohup gunicorn -w 1 -b 0.0.0.0:5000 app:app &