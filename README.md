# Campus-Event-Management-System

I have created a simple prototype for campus events management using the below tech stacks:
1. Python
2. Flask
3. REST api using Flask
4. SQLite

The API can be tested using postman or curl

Right now there is no seperate modules integrated for admin and students. I have assumed that In real world scenario, the admin will have seperate credentials and privileges. But only for prototype i just assumed that create event API is only exposed to admin and use by them.

Admin responsibilty is to create an event.

Student responsiblities include registering for event, marking attendance, and submitting  feedback.

No login/authentication → I keep it simple for the assignment.
One Flask app handles both roles → APIs decide what each role can do.
Admin → Uses /event
Student → Uses /student, /register, /attendance, /feedback

Future scope includes fully functioning web app for admin and mobile app for the students.

To run the app
pip install flask (if not already installed)
python app.py

API can be used using POST or GET
