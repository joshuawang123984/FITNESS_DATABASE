from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .logic import *

import tkinter as tk
from tkinter import ttk, messagebox

from .global_funcs import reset_tables, create_buttons

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
            create_buttons(self, self.button_frame, self.all_buttons_names, self.button_refs, self.cmnds, self.session, self.engine, 'member', self.curr_member_id)
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
            create_buttons(self, self.button_frame, self.all_buttons_names, self.button_refs, self.cmnds, self.session, self.engine, 'trainer', self.curr_trainer_id)
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
            create_buttons(self, self.button_frame, self.all_buttons_names, self.button_refs, self.cmnds, self.session, self.engine, 'admin', self.curr_admin_id)
            self.curr_admin_label.config(text=f"CURR ADMIN_ID: {admin_id}")
        else:
            messagebox.showwarning("Warning", f"ADMIN ID {admin_id} DOES NOT EXIST IN DATABASE")
            self.curr_admin_id = None
            self.controller.show_frame(MainMenu)
        
if __name__ == '__main__':
    main()

#TEST FUNCTIONALITY OF BUTTONS