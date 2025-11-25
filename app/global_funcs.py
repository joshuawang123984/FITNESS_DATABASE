from sqlalchemy import text

from .logic import *

import tkinter as tk
from tkinter import ttk

from tkinter import simpledialog
from functools import partial
import inspect
from datetime import datetime

def reset_tables(engine, session):
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            #delete all rows in correct order
            conn.execute(text("DELETE FROM billing"))
            conn.execute(text("DELETE FROM group_training_session"))
            conn.execute(text("DELETE FROM training_session"))
            conn.execute(text("DELETE FROM room_booking"))
            conn.execute(text("DELETE FROM goal"))
            conn.execute(text("DELETE FROM health_metrics"))
            conn.execute(text("DELETE FROM member"))
            conn.execute(text("DELETE FROM trainer"))
            conn.execute(text("DELETE FROM admin"))
            
            #reset sequences count
            sequences = [
                "member_member_id_seq",
                "trainer_trainer_id_seq",
                "admin_admin_id_seq",
                "health_metrics_metric_id_seq",
                "goal_goal_id_seq",
                "training_session_session_id_seq",
                "group_training_session_session_id_seq",
                "room_booking_room_id_seq",
                "billing_bill_id_seq"
            ]
            for seq in sequences:
                conn.execute(text(f"ALTER SEQUENCE {seq} RESTART WITH 1"))

            trans.commit()
            print("All tables cleared and sequences reset.")
        except Exception as e:
            trans.rollback()
            print("Failed to clear tables:", e)
            raise

    #creates a default admin row
    existing = session.query(Admin).first()

    if not existing:
        default_admin = Admin(
            name="default_admin",
            email="admin123@gmail.com" 
        )
        session.add(default_admin)
        session.commit()
        print("Default admin created.")
    else:
        print("Admin already exists.")

def create_buttons(root, button_frame, all_buttons_names, button_refs, cmnds, session, engine, page, user_id):
        row, col = 0, 0
        for i, name in enumerate(all_buttons_names):
            #find the function, and request these parameters from the user
            sig = inspect.signature(cmnds[i])
            param_names = list(sig.parameters.keys())
            param_str = ", ".join(param_names[1:])

            #create each button, put it on the frame at coords (row, col), then give it functionality
            if page == 'admin':
                button_refs[name] = create_button(button_frame, name, row, col, 10, partial(create_dialog_admin, root, i, name, param_str, session, engine, cmnds, user_id))
            elif page == 'member':
                button_refs[name] = create_button(button_frame, name, row, col, 10, partial(create_dialog_member, root, i, name, param_str, session, engine, cmnds, user_id))
            elif page == 'trainer':
                button_refs[name] = create_button(button_frame, name, row, col, 10, partial(create_dialog_trainer, root, i, name, param_str, session, engine, cmnds, user_id))

            if col > (col + 1) % 3:
                row += 1
            col = (col + 1) % 3

def create_button(root, name, row, col, padx, cmnd):
        btn = ttk.Button(root, text=name, command=cmnd)
        btn.grid(row=row, column=col, padx=padx)
        return btn

def create_dialog_admin(root, i, name, textt, session, engine, cmnds, admin_id):
    text = textt
    data_type_conversions = get_data_type_conversions()
    requires_admin = False

    if text[:8] == 'admin_id':
        text = text[10:]
        requires_admin = True
    
    if cmnds[i] == reset_tables:
        process_requests(root, cmnds[i], [engine, session])
        return

    inp = simpledialog.askstring("Enter params (if empty,click ok!): ", text, parent=root)

    args = [session]
    if requires_admin:
        args += [admin_id]
    args += [arg.strip() for arg in inp.split(',') if arg.strip()]
    
    for idx, a in enumerate(text.split(',')):
        if (param := a.strip()) in data_type_conversions:
            try:
                if requires_admin:
                    args[idx+2] = data_type_conversions[param](args[idx+2])
                else:
                    args[idx+1] = data_type_conversions[param](args[idx+1])
            except (IndexError):
                continue

    process_requests(root, cmnds[i], args)

def create_dialog_member(root, i, name, textt, session, engine, cmnds, member_id):
    text = textt
    data_type_conversions = get_data_type_conversions()
    requires_member = False

    if text[:9] == 'member_id':
        text = text[11:]
        requires_member = True

    inp = simpledialog.askstring("Enter params (if empty,click ok!): ", text, parent=root)

    args = [session]
    if requires_member:
        args += [member_id]
    args += [arg.strip() for arg in inp.split(',') if arg.strip()]

    for idx, a in enumerate(text.split(',')):
        if (param := a.strip()) in data_type_conversions:
            try:
                if requires_member:
                    args[idx+2] = data_type_conversions[param](args[idx+2])
                else:
                    args[idx+1] = data_type_conversions[param](args[idx+1])
            except (IndexError):
                continue
    
    process_requests(root, cmnds[i], args)

def create_dialog_trainer(root, i, name, textt, session, engine, cmnds, trainer_id):
    text = textt
    data_type_conversions = get_data_type_conversions()
    requires_trainer = False

    if text[:10] == 'trainer_id':
        text = text[12:]
        requires_trainer = True

    inp = simpledialog.askstring("Enter params (if empty,click ok!): ", text, parent=root)

    args = [session]
    if requires_trainer:
        args += [trainer_id]
    args += [arg.strip() for arg in inp.split(',') if arg.strip()]

    for idx, a in enumerate(text.split(',')):
        if (param := a.strip()) in data_type_conversions:
            try:
                if requires_trainer:
                    args[idx+2] = data_type_conversions[param](args[idx+2])
                else:
                    args[idx+1] = data_type_conversions[param](args[idx+1])
            except (IndexError):
                continue

    process_requests(root, cmnds[i], args)

def convert_status(status):
    return True if status == 'active' else False

def get_data_type_conversions():
    data_type_conversions = {
        'amount': int,
        'height_cm': int,
        'mass_kg': float,
        'target_bf_percentage': float,
        'target_mass_kg': float,
        'num_participants': int,
        'dob': partial(lambda s, fmt: datetime.strptime(s, fmt).date(), fmt="%Y-%m-%d"),
        'start_date': partial(lambda s, fmt: datetime.strptime(s, fmt).date(), fmt="%Y-%m-%d"),
        'end_date': partial(lambda s, fmt: datetime.strptime(s, fmt).date(), fmt="%Y-%m-%d"),
        'date_taken': partial(lambda s, fmt: datetime.strptime(s, fmt).date(), fmt="%Y-%m-%d"),
        'start_time': partial(lambda s, fmt: datetime.strptime(s, fmt), fmt="%Y-%m-%d %H:%M:%S"),
        'end_time': partial(lambda s, fmt: datetime.strptime(s, fmt), fmt="%Y-%m-%d %H:%M:%S"),
        'bill_status': convert_status,
        'used_status': convert_status
    }
    return data_type_conversions

def get_my_objs():
    my_objs = {Member, Trainer, Admin, HealthMetrics, Goal, TrainingSession, GroupTrainingSession, RoomBooking, Billing}
    return my_objs

def process_requests(root, cmnd, args):
    #if user wants to see information, then get results from functions:
    my_objs = get_my_objs()
    
    cmnd(*args)
    if cmnd is get_dashboard:

        #HARDCODED FOR get_dashboard
        tables = ['TrainingSession', 'Goal', 'HealthMetrics', 'Member']
        results = {table: set() for table in tables}
        for row in cmnd(*args):
            for val in row:
                if val is None:
                    continue
                if type(val) in my_objs:
                    #print(f"\nObject type: {type(val).__name__}")
                    temp = tuple(getattr(val, column.name) for column in type(val).__table__.columns)
                else:
                    temp = tuple(val)
                
                results[type(val).__name__].add(temp)
        
        #create a view for each thing you want user to see (trainingsession, goals, healthmetrics)
        for table in tables:
            if table == 'Member':
                continue
            
            create_user_view(root, table, [c.name for c in (globals()[table].__table__.columns)], results[table])

    elif cmnd is get_schedule:
        #HARDCODED FOR get_schedule
        tables = ['TrainingSession', 'GroupTrainingSession']
        results = {table: set() for table in tables}
        for obj in cmnd(*args): 
            if obj is None:
                continue
            if type(obj) in my_objs:
                temp = tuple(getattr(obj, column.name) for column in type(obj).__table__.columns)
                results[type(obj).__name__].add(temp)
                
        for table in tables:
            create_user_view(root, table, [c.name for c in (globals()[table].__table__.columns)], results[table])

def create_user_view(root, name, columns, results):
    popup = tk.Toplevel(root)
    popup.title(f"USER VIEW ( {name} DASHBOARD)")

    tree = ttk.Treeview(popup, columns=columns, show='headings')
    tree.pack(fill='both', expand=True, padx=10, pady=10)
  
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for row in results:
        if row:
            tree.insert('', 'end', values=row)

    close_btn = tk.Button(popup, text="Close", command=popup.destroy)
    close_btn.pack(pady=5)