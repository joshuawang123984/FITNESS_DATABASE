# FITNESS DATABASE FINAL PROJECT

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

#CASES TO TEST:
Adding of Member, Trainer, Goal, TrainingSession, GroupTrainingSession, HealthMetric, Goal, Room, Billing 
Removal of Member, Trainer, Goal, TrainingSession, GroupTrainingSession, HealthMetric, Goal, Room, Billing (with various combinations of parameters)

Test adding sessions to rooms at overlapping times

Views of DashBoard and Schedule for various Members
Changes to dependencies after removals (eg: removing a room would remove corresponding trainingsessions using that room)

#TO DO:
Must add an admin class, modify the drawio, implement this admin class
might have to change the ui to allow for 3 types of logins, which will invenitabily affect button visibility for each user

prev remove_member():
@staticmethod
def remove_member(session, member_id=None, name=None, dob=None, gender=None, email=None, phone=None):
    filters = []
    if member_id:
        filters.append(Member.member_id == member_id)
    if name and dob and gender:
        filters.append(and_(Member.name == name, Member.date_of_birth == dob, Member.gender == gender))
    if email:
        filters.append(Member.email == email)
    if phone:
        filters.append(Member.phone_number == phone)

    member = session.query(Member).filter(or_(*filters)).first()
    if member:
        try:
            types = [Billing, TrainingSession, HealthMetrics, Goal]
            attribute = 'member_id'
            for type in types:
                _delete_from_other_tables(session, type, attribute, member_id)
            
            _safe_delete(member)
            session.delete(member)
            session.commit()
        except Exception as e:
            session.rollback()