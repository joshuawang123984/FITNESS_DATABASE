
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

ORM was used throughout this project to define and manage the eight database tables: Member, Trainer, HealthMetrics, Goal, TrainingSession, GroupTrainingSession, RoomBooking, and Billing directly through Python classes rather than writing raw SQL for every operation. Using SQLAlchemy’s ORM layer, each table is represented as a class with attributes corresponding to the columns, and relationships are defined with foreign keys and ORM relationship objects. This approach allows the program to automatically translate Python object manipulations (creating, deleting, updating) into the correct SQL statements. For example, creating a new member or scheduling a training session simply involves instantiating the class and committing it to the session with SQLAlchemy handling insertion into PostgreSQL.

The ORM was also used heavily in the logic behind user operations in the Tkinter interface, particularly for enforcing constraints and cascading effects. When the user performs actions such as deleting a room, updating billing status, or adding a session, the ORM manages relationship rules such as cascading deletes or preventing invalid insertions (for example, two sessions booking the same room at the same time). Queries like retrieving dashboards, checking trainer schedules, or filtering sessions are executed through high-level ORM query methods rather than handwritten SQL. This made the project easier to scale, since SQLAlchemy ensures that all table interactions respect the schema and relationships defined in the model classes.

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

TESTCASES:
Adding to each table
Ensuring proper additions to table (ie: adding a trainingsession at the same time as another shouldnt add to the table)
Removals of elements from each table
Removals of dependencies of said element (ie: removal of room removes all trainingsessions in that room)

UserViews (getdashboard, getschedule)
Updates to the tables (paying bills)
reset tables
