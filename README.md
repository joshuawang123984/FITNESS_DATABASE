# FITNESS DATABASE FINAL PROJECT
Name: Joshua Wang
SN: 101307312
PROJ GROUP: 38

This program creates 8 tables and stores them in a database.
The program creates 8 different tables:
- Member
- Trainer
- HealthMetrics
- Goal
- TrainingSession
- GroupTrainingSession
- RoomBooking
- Billing

A user interface is then created and allows users to modify these tables, with operations such as adding, removing, viewing.

Requirements:
tkinter
Python3
PostgreSQL
sqlalchemy library

Opening DB in terminal: 
psql -U postgres -h localhost -d main_fitness_DB

Steps to Run:
1. Go into Fitness_Database directory
2. run python3 -m app in terminal
3. to start fresh, click the button "delete tables", then "create_tables"
4. Click the buttons and follow the argument input instructions on the simpledialog
5. Open the database through your terminal or database management tool to see changes

User input for each parameter FORMATTING:

        'amount': int,
        'height_cm': int,
        'mass_kg': float,
        'target_bf_percentage': float,
        'target_mass_kg': float,
        'num_participants': int,
        'dob': fmt="%Y-%m-%d",
        'start_date': fmt="%Y-%m-%d",
        'end_date': fmt="%Y-%m-%d",
        'date_taken': fmt="%Y-%m-%d",
        'start_time': fmt="%Y-%m-%d %H:%M:%S",
        'end_time': fmt="%Y-%m-%d %H:%M:%S",
        'bill_status': 'active' or 'inactive',
        'used_status': 'active' or 'inactive',
        'session_type': 'personal' or anything else is group_training_session

#TO NOTE:
used_status in room_booking class is unused.

Potential Adjustments:
Many of the global_funcs have parameters that are unnecessary/unefficient ie: passing in cmnds and i in create_dialog rather than cmnds[i] (passing in a list and idx rather than the element at the list)

Maybe when creating the buttons, split them up into 2 parts - creation and removals, and other
during the video, can add get_dashboard to the trainers section of the page to make it work

TESTCASES:
Adding to each table
Ensuring proper additions to table (ie: adding a trainingsession at the same time as another shouldnt add to the table)
Removals of elements from each table
Removals of dependencies of said element (ie: removal of room removes all trainingsessions in that room)

UserViews (getdashboard, getschedule)
Updates to the tables (paying bills)
reset tables

video link: 
first vid: https://vimeo.com/1140590108?share=copy&fl=sv&fe=ci
second vid: https://vimeo.com/1140589232?share=copy&fl=sv&fe=ci
