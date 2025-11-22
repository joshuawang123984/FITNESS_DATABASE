from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from .logic import *
from models.AllModels import get_base

import tkinter as tk
from tkinter import ttk, messagebox

from tkinter import simpledialog
from functools import partial
import inspect
from datetime import datetime
def reset_tables(engine, session):
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            # Delete all rows in correct order
            conn.execute(text("DELETE FROM billing"))
            conn.execute(text("DELETE FROM room_booking"))
            conn.execute(text("DELETE FROM group_training_session"))
            conn.execute(text("DELETE FROM training_session"))
            conn.execute(text("DELETE FROM goal"))
            conn.execute(text("DELETE FROM health_metrics"))
            conn.execute(text("DELETE FROM member"))
            conn.execute(text("DELETE FROM trainer"))
            conn.execute(text("DELETE FROM admin"))
            
            # Reset sequences
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

def convert_status(status):
    return True if status == 'active' else False

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

def main():
    connection_name = 'postgresql://postgres:Joshua26%40joshua@localhost:5432/main_fitness_DB'
    engine = create_engine(connection_name)
    print("Connection successful" if engine else "Connection failed")
     
    Session = sessionmaker(bind=engine)
    session = Session()

    app = App(session, engine)
    app.mainloop()

class App(tk.Tk):
    def __init__(self, session, engine):
        super().__init__()

        self.title("FITNESS DB UI")
        self.geometry("600x800")

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}

        for F in (MainMenu, Page1, Page2, Page3):
            frame = F(container, self, session, engine)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainMenu)

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()

"""------------------------------------------------------------------------------------------------------------------------------
------------------------------------------ --------   FRAMES --------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------"""
class MainMenu(ttk.Frame):
    def __init__(self, parent, controller, session, engine):
        super().__init__(parent)
        self.session = session
        self.engine = engine

        ttk.Label(self, text="Main Menu", font=("Arial", 20)).pack(pady=20)

        ttk.Button(self, text="MEMBER",
                   command=lambda: controller.show_frame(Page1)).pack(pady=10)

        ttk.Button(self, text="TRAINER",
                   command=lambda: controller.show_frame(Page2)).pack(pady=10)

        ttk.Button(self, text="ADMIN",
                   command=lambda: controller.show_frame(Page3)).pack(pady=10)
        
        ttk.Button(self, text="EXIT", 
                   command=lambda: controller.destroy()).pack(pady=10)


class Page1(ttk.Frame):
    def __init__(self, parent, controller, session, engine):
        super().__init__(parent)
        self.session = session
        self.engine = engine
        self.controller = controller
        self.curr_member_id = None

        ttk.Label(self, text="MEMBER", font=("Arial", 20)).grid(row=0, column=0, padx=10)

        ttk.Button(self, text="Back to Menu",
                    command=lambda: controller.show_frame(MainMenu)).grid(row=1, column=0, padx=10)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=2, column=0, pady=50)

        self.button_refs = {}
        self.all_buttons_names = ['create_goal', 'remove_goal', 'create_health_metric', 'remove_health_metric', 'update_profile', 
                        'get_dashboard', 'pay_bill']
        self.cmnds = [create_goal, remove_goal, create_health_metric, 
            remove_health_metric, update_profile, get_dashboard, pay_bill]
        
        self.id_frame = ttk.Frame(self)
        self.id_frame.grid(row=3, column=0, pady=20)
        
        self.id_var = tk.StringVar()
        ttk.Label(self.id_frame, text="Enter Member ID:").grid(row=0, column=0, padx=5)
        ttk.Entry(self.id_frame, textvariable=self.id_var, width=15).grid(row=0, column=1, padx=5)
        ttk.Button(self.id_frame, text="Submit", command=self.check_member_id).grid(row=0, column=2, padx=5)

        self.curr_member_label = ttk.Label(self.id_frame, text="")
        #the row val doesnt matter, just has to be at the bottom so that doesnt overlap buttons
        self.curr_member_label.grid(row=10, column=0, padx=5)

    def check_member_id(self):
        member_id = self.id_var.get().strip()
        result = self.session.query(Member).filter(Member.member_id == int(member_id)).first()

        if result:
            self.curr_member_id = int(self.id_var.get())
            create_buttons(self, self.button_frame, self.all_buttons_names, self.button_refs, self.cmnds, self.session, self.engine)
            self.curr_member_label.config(text=f"CURR MEMBER_ID: {member_id}")
        else:
            messagebox.showwarning("Warning", f"Member ID {member_id} DOES NOT EXIST IN DATABASE")
            self.curr_member_id = None
            self.controller.show_frame(MainMenu)

class Page2(ttk.Frame):
    def __init__(self, parent, controller, session, engine):
        super().__init__(parent)
        self.session = session
        self.engine = engine

        ttk.Label(self, text="TRAINER", font=("Arial", 20)).grid(row=0, column=0, padx=10)
        ttk.Button(self, text="Back to Menu",
                   command=lambda: controller.show_frame(MainMenu)).grid(row=1, column=0, padx=10)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=2, column=0, pady=50)

        self.button_refs = {}
        self.all_buttons_names = ['create_training_session', 'remove_training_session', 'create_group_training_session', 
                                  'remove_group_training_session', 'get_schedule']
    
        self.cmnds = [create_training_session, remove_training_session, 
             create_group_training_session, remove_group_training_session, get_schedule]
        
        self.id_frame = ttk.Frame(self)
        self.id_frame.grid(row=3, column=0, pady=20)
        
        self.id_var = tk.StringVar()
        ttk.Label(self.id_frame, text="Enter Trainer ID:").grid(row=0, column=0, padx=5)
        ttk.Entry(self.id_frame, textvariable=self.id_var, width=15).grid(row=0, column=1, padx=5)
        ttk.Button(self.id_frame, text="Submit", command=self.check_trainer_id).grid(row=0, column=2, padx=5)

        self.curr_trainer_label = ttk.Label(self.id_frame, text="")
        self.curr_trainer_label.grid(row=10, column=0, padx=5)

    def check_trainer_id(self):
        trainer_id = self.id_var.get().strip()
        result = self.session.query(Trainer).filter(Trainer.trainer_id == int(trainer_id)).first()

        if result:
            self.curr_trainer_id = int(self.id_var.get())
            create_buttons(self, self.button_frame, self.all_buttons_names, self.button_refs, self.cmnds, self.session, self.engine)
            self.curr_trainer_label.config(text=f"CURR TRAINER_ID: {trainer_id}")
        else:
            messagebox.showwarning("Warning", f"TRAINER ID {trainer_id} DOES NOT EXIST IN DATABASE")
            self.curr_trainer_id = None
            self.controller.show_frame(MainMenu)


class Page3(ttk.Frame):
    def __init__(self, parent, controller, session, engine):
        super().__init__(parent)
        self.session = session
        self.engine = engine

        ttk.Label(self, text="ADMIN", font=("Arial", 20)).grid(row=0, column=0, pady=20)
        ttk.Button(self, text="Back to Menu",
                   command=lambda: controller.show_frame(MainMenu)).grid(row=1, column=0, pady=20)

        self.button_frame = ttk.Frame(self)
        self.button_frame.grid(row=2, column=0, pady=50)

        self.button_refs = {}
        self.all_buttons_names = ['register_member', 'remove_member', 'register_trainer', 'remove_trainer', 'create_training_session', 
                         'remove_training_session', 'create_group_training_session', 'remove_group_training_session','get_dashboard', 
                         'get_schedule', 'add_room', 'remove_room', 'book_room', 
                        'generate_bill', 'pay_bill', 'reset_tables']
    
        self.cmnds = [register_member, remove_member, register_trainer, remove_trainer, create_training_session, 
                      remove_training_session, 
             create_group_training_session, remove_group_training_session, get_dashboard, get_schedule, add_room, 
             remove_room, book_room, generate_bill, pay_bill, reset_tables]
        
        self.id_frame = ttk.Frame(self)
        self.id_frame.grid(row=3, column=0, pady=20)
        
        self.id_var = tk.StringVar()
        ttk.Label(self.id_frame, text="Enter ADMIN ID:").grid(row=0, column=0, padx=5)
        ttk.Entry(self.id_frame, textvariable=self.id_var, width=15).grid(row=0, column=1, padx=5)
        ttk.Button(self.id_frame, text="Submit", command=self.check_admin_id).grid(row=0, column=2, padx=5)

        self.curr_admin_label = ttk.Label(self.id_frame, text="")
        self.curr_admin_label.grid(row=10, column=0, padx=5)
    
    def check_admin_id(self):
        admin_id = self.id_var.get().strip()
        result = self.session.query(Admin).filter(Admin.admin_id == int(admin_id)).first()

        if result:
            self.curr_admin_id = int(self.id_var.get())
            create_buttons(self, self.button_frame, self.all_buttons_names, self.button_refs, self.cmnds, self.session, self.engine)
            self.curr_admin_label.config(text=f"CURR ADMIN_ID: {admin_id}")
        else:
            messagebox.showwarning("Warning", f"ADMIN ID {admin_id} DOES NOT EXIST IN DATABASE")
            self.curr_admin_id = None
            self.controller.show_frame(MainMenu)
        
def create_buttons(root, button_frame, all_buttons_names, button_refs, cmnds, session, engine):
        row, col = 0, 0
        for i, name in enumerate(all_buttons_names):
            #find the function, and request these parameters from the user
            sig = inspect.signature(cmnds[i])
            param_names = list(sig.parameters.keys())
            param_str = ", ".join(param_names[1:])

            #create each button, put it on the frame at coords (row, col), then give it functionality
            button_refs[name] = create_button(button_frame, name, row, col, 10, partial(create_dialog, root, i, name, param_str, session, engine, cmnds))
            if col > (col + 1) % 3:
                row += 1
            col = (col + 1) % 3

def create_button(root, name, row, col, padx, cmnd):
        btn = ttk.Button(root, text=name, command=cmnd)
        btn.grid(row=row, column=col, padx=padx)
        return btn

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

def create_dialog(root, i, name, text, session, engine, cmnds):
            data_type_conversions = get_data_type_conversions()
            my_objs = get_my_objs()

            inp = simpledialog.askstring("Enter params (if empty,click ok!): ", text, parent=root)
            args = [session] + [arg.strip() for arg in inp.split(',') if arg.strip()]
            
            if cmnds[i] == reset_tables:
                args = [engine, session]

            for idx, a in enumerate(text.split(',')):
                if (param := a.strip()) in data_type_conversions:
                    try:
                        args[idx+1] = data_type_conversions[param](args[idx+1])
                    except (IndexError):
                        continue
              
            #if user wants to see information, then get results from functions:
            cmnds[i](*args)
            if cmnds[i] is get_dashboard:
      
                #HARDCODED FOR get_dashboard
                tables = ['TrainingSession', 'Goal', 'HealthMetrics', 'Member']
                results = {table: set() for table in tables}
                for row in cmnds[i](*args):
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

            elif cmnds[i] is get_schedule:
                #HARDCODED FOR get_schedule
                tables = ['TrainingSession', 'GroupTrainingSession']
                results = {table: set() for table in tables}
                for obj in cmnds[i](*args): 
                    if obj is None:
                        continue
                    if type(obj) in my_objs:
                        temp = tuple(getattr(obj, column.name) for column in type(obj).__table__.columns)
                        results[type(obj).__name__].add(temp)
                       
                for table in tables:
                    create_user_view(root, table, [c.name for c in (globals()[table].__table__.columns)], results[table])

if __name__ == '__main__':
    main()

#TEST FUNCTIONALITY OF BUTTONS
#For operations that involve id, if the id is given (youre logged in, then can pass in the curr_id )
#for each page, the curr id is already stored, just pass that in then when creating the buttons.
#also, room_booking doesnt need admin_id as an attribute. can be removed after testing
#add try except for each logic with session.rollback() if it fails
#if there are problems with this session rollback addition, change back to og (move the creation of row vlaue in try statement)