How to use CalendarMe:

[Introduction]
CalendarMe is a centralized calendar application that allows both students and teachers to access homework and assignment deadlines.
This enables students to keep track of the upcoming weeks deadlines for each subject, whilst allowing teachers to dynamically update
the submission dates across the weeks. Furthermore, teachers are able to cater deadlines to meet the needs of the students throughout
the week. For example, if a specific day in the week, lets say Tuesday already has 2 submissions due, the teacher of another subject,
would be able to shift their deadline to another day in order to allow students ample time to complete their work, reducing the chance
of conflicting deadlines. The system consists of 2 Python files, the first is an application that is to be used on the Raspberry Pi
with the touchscreen and breadboard with buttons attached to it. While the second  is to be run on a separate computer. 

[DW 1D app.py]
This file is to be run on the Raspberry Pi. This is a simple GUI that allows the teacher to add events to the centralized calendar.
It features a set of buttons that allows the user to select the subject and key in essential information regarding the submission.
Teachers will be able to dynamically and constantly add new deadlines whenever required.

- How it works -
The app makes use of multiple modules including KIVY, Firebase and the built-in Raspberry Pi modules available to Python.

1. Initialise Firebase with the respective url and apikey. Instantiate the database to db
2. Initialise the GPIO buttons on the Raspberry Pi assigning buttons to their respective subjects and an additional button that launches
   the application when pressed
3. Build UI
	a. Create description_selection, date_selection, time_selection, MyLabel as Custom Widgets that will be added later to the layout
	b. Initialise the Starting Screen which Consists of Subject and their corresponding colour tags
	c. Define 2 functions, change_screen() that changes the screen of the app, and checker() which runs change_screen() when buttons are pressed
	d. Run an internal clock that checks every 0.1secs whether the GPIO buttons are pressed
	e. Screen 2 consists of all the Custom Widgets as mentioned in 1. these widgets enable the user to key in the description and due date
	   of the assignments
	f. Define 3 functions, subject_change() which changes a label to indicate which subject has been selected and upload() which uploads the 
	   formatted information to firebase.
	g. FinalApp adds both Screens to a Screen Manager and returns that GUI
4. Constantly runs a function main() that constantly checks whether the button to add submissions is pressed and runs the app when it does.

[trial_event.py]
This file is to be run on a separate computer. The program here checks firebase for any added submissions and if there exist new entries, add
then to the centralized calendar.

- How it works -
1. Initialise the authentification for user using Google Calendars API (Done so by checking the Authentification .json file that exist within
   the local computer)
2. Initialise Firebase with the respective url and apikey. Instantiate the database to db
3. Define a main() loop that continuously checks if there are new events that populate the firebase database
4. Define a calendar_add() function that formats the information into a format that Google Calendar is able to recognise and removes the
   information from the databse once it is added
5. Run the main() function once to start the sequence.