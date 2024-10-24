Challenge1: University of Florida did not allow Microsoft teams shifts to sync with any calendar. This led to students manually adding their work shifts to their calendar. Students also had challenges calculating their scheduled hours. Especially for international students who could not exceed the 20 hour limit cap.

Solution: Using microsoft workflows, I scanned user shifts(per user) for the next two weeks and sent them to their google calendar. Users need to do a one time integration between teams and calendar.

Challenge 2: The workflow rules had very limited control, I was not able to send uniquely added calendar events. For practicality, every day at 6pm, the shifts will be sent to google calendar. 

Challenge 3: Google calendar does not recognize the duplicate entries as eventId is different even if event Name, start time, end time are the same. How can we delete duplicate calendar events. 

Solution: Using google calendar api, we can get a list of all the events in a time period. Identifying events with same name and starttime and endtime, we can delete the duplicate ones. This process can be executed every day at 6:30 pm. 

Challenge: How do we automate this script?

Solution: Flask app on ec2 instance. The api endpoint is invoked by an aws event bridge function.  

Flow: Users sign in to the hosted website, do a one time google Auth. They can view their shifts report. 

Additional Functionality: This Workflow is also integrated with slack using a slack app. If the user ever exceeds their permitted hours, can send an notification. Integrating to other applications should not be challenging. 


Deployment:
Code changes once approved, using github workflows+aws code pipeline are deployed to the ec2 instance. Right now, the service has a single ec2 instance running so the service shuts down for a few seconds during deployment. 
