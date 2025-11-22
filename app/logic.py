from models.AllModels import Member, Trainer, Admin, HealthMetrics, Goal, TrainingSession, GroupTrainingSession, RoomBooking, Billing
from sqlalchemy import and_, or_

def _delete_from_other_tables(session, type, attr, value):
    session.query(type).filter(getattr(type, attr) == value).delete(synchronize_session='fetch')
    session.commit()
            # temp = session.query(type).filter(
            #     getattr(type, attr) == value
            # ).all()

            # for t in temp:
            #     _safe_delete(session, t)
                # session.delete(t)

def _find_overlap(session, room_id, start_time, end_time, type):
    overlap_exists = session.query(type).filter(
            and_(
                type.room_id == room_id,
                type.start_time < end_time,
                type.end_time > start_time
            )
        ).first()

    if overlap_exists:
        return True
        
def _safe_add(session, var):
    try:
        session.add(var)
        session.commit()
        return var
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

def _safe_delete(session, var):
    try:
        session.delete(var)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error: {e}")

@staticmethod
def register_member(session, name, dob, gender, email, phone):
    new_member = Member(name=name, date_of_birth=dob, gender=gender, email=email, phone_number=phone)

    _safe_add(session, new_member)

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
        types = [Billing, TrainingSession, HealthMetrics, Goal]
        attribute = 'member_id'
        for type in types:
            _delete_from_other_tables(session, type, attribute, member_id)
        
        _safe_delete(session, member)

@staticmethod
def register_trainer(session, name, dob, email, phone):
    new_trainer = Trainer(name=name, date_of_birth=dob, email=email, phone_number=phone)

    _safe_add(session, new_trainer)

@staticmethod
def remove_trainer(session, trainer_id, name=None, dob=None, email=None, phone=None):
    filters = []
    if trainer_id:
        filters.append(Trainer.trainer_id == trainer_id)
    if name and dob:
        filters.append(and_(Trainer.name == name, Trainer.date_of_birth == dob))
    if email:
        filters.append(Trainer.email == email)
    if phone:
        filters.append(Trainer.phone_number == phone)

    trainer = session.query(Trainer).filter(or_(*filters)).first()
    if trainer:
        types = [TrainingSession, GroupTrainingSession]
        attribute = 'trainer_id'
        for type in types:
            _delete_from_other_tables(session, type, attribute, trainer_id)

        _safe_delete(session,trainer)
           
@staticmethod
def create_training_session(session, room_id, member_id, trainer_id, start_time, end_time):

    if _find_overlap(session, room_id, start_time, end_time, TrainingSession):
        print("ROOM IS BEING USED AT THIS TIME!!!")
        return None
    
    new_training_session = TrainingSession(room_id=room_id, member_id=member_id, trainer_id=trainer_id, start_time=start_time, end_time=end_time)
    _safe_add(session, new_training_session)

@staticmethod
def remove_training_session(session, room_id, start_time=None, end_time=None):
    filters = []

    if room_id and start_time:
        filters.append(and_(TrainingSession.room_id == room_id, TrainingSession.start_time == start_time))

    if room_id and end_time:
        filters.append(and_(TrainingSession.room_id == room_id, TrainingSession.end_time == end_time))

    training_session = session.query(TrainingSession).filter(or_(*filters)).first()
    if training_session:
        _safe_delete(session, training_session)

@staticmethod
def create_group_training_session(session, room_id, trainer_id, start_time, end_time, num_participants):

    if _find_overlap(session, room_id, start_time, end_time, GroupTrainingSession):
        print("ROOM IS BEING USED AT THIS TIME!!!")
        return None
    
    new_group_training_session = GroupTrainingSession(room_id=room_id,trainer_id=trainer_id, start_time=start_time, end_time=end_time, num_participants=num_participants)
    _safe_add(session, new_group_training_session)

@staticmethod
def remove_group_training_session(session, room_id, start_time=None, end_time=None):
    filters = []

    if room_id and start_time:
        filters.append(and_(GroupTrainingSession.room_id == room_id, GroupTrainingSession.start_time == start_time))

    if room_id and end_time:
        filters.append(and_(GroupTrainingSession.room_id == room_id, GroupTrainingSession.end_time == end_time))

    training_session = session.query(GroupTrainingSession).filter(or_(*filters)).first()
    if training_session:
        _safe_delete(training_session)

@staticmethod
def create_goal(session, member_id, target_mass_kg, target_bf_percentage, start_date, end_date):
    new_goal = Goal(member_id=member_id, target_mass_kg=target_mass_kg, target_bf_percentage=target_bf_percentage, start_date=start_date, end_date=end_date)
    
    _safe_add(session, new_goal)

@staticmethod
def remove_goal(session, member_id, start_date=None, end_date=None):
    filters = []
    if member_id and start_date:
        filters.append(and_(Goal.member_id == member_id, Goal.start_date == start_date))
    if member_id and end_date:
        filters.append(and_(Goal.member_id == member_id, Goal.end_date == end_date))

    goal = session.query(Goal).filter(or_(*filters)).first()
    if goal:
        _safe_delete(session, goal)

@staticmethod
def create_health_metric(session, member_id, height_cm, mass_kg, heart_rate, date_taken):
    new_health_metric = HealthMetrics(member_id=member_id, height_cm=height_cm, mass_kg=mass_kg, heart_rate=heart_rate, date_taken=date_taken)

    _safe_add(session, new_health_metric)

@staticmethod
def remove_health_metric(session, member_id, date_taken):
    health_metric = session.query(HealthMetrics).filter(
    and_(HealthMetrics.member_id == member_id, HealthMetrics.date_taken == date_taken)
    ).first()
    if health_metric:
        _safe_delete(session, health_metric)

@staticmethod
def update_profile(session, member_id, name=None, phone=None):
    member = session.get(Member, member_id)
    if name: member.name = name
    if phone: member.phone_number = phone
    session.commit()

@staticmethod
def get_dashboard(session, member_id):
    return (
        session.query(Member, HealthMetrics, Goal, TrainingSession)
        .filter(Member.member_id == member_id)
        .outerjoin(Member.health_metrics)
        .outerjoin(Member.goals)
        .outerjoin(Member.training_sessions)
        .all()
    )

@staticmethod
def get_schedule(session, trainer_id):
    solo_sessions = session.query(TrainingSession).filter_by(trainer_id=trainer_id).all()
    group_sessions = session.query(GroupTrainingSession).filter_by(trainer_id=trainer_id).all()
    return solo_sessions + group_sessions

@staticmethod
def add_room(session, room_id):
    new_room = RoomBooking(room_id=room_id, used_status=False)
    _safe_add(session, new_room)

@staticmethod
def remove_room(session, room_id):
    
    room = session.query(RoomBooking).filter(
        (RoomBooking.room_id == room_id)
    ).first()
    if room:
        #for each group training session and training session, remove if room_id = room_id
        types = [TrainingSession, GroupTrainingSession]
        attribute = 'room_id'
        for type in types:
            _delete_from_other_tables(session, type, attribute, room_id)
        
        #delete room last otherwise the other stuff cant find the entry with room_id = room_id if deleted
        _safe_delete(session, room)

@staticmethod
def book_room(session, room_id, session_type, member_id, trainer_id, start_time, end_time):
    if session_type == "personal":
        session_data = TrainingSession(room_id=room_id, member_id=member_id, trainer_id=trainer_id,
                                      start_time=start_time, end_time=end_time)
    else:
        session_data = GroupTrainingSession(room_id=room_id, trainer_id=trainer_id,
                                           start_time=start_time, end_time=end_time, num_participants=0)
    room = session.query(RoomBooking).get(room_id)

    if not room:
        print('no such room')
        return
    if room.used_status:
        raise ValueError('Room already booked')
    #room.used_status = True
    _safe_add(session, session_data)
    # session.add(session_data)
    # session.commit()

@staticmethod
def generate_bill(session, member_id, amount):
    bill = Billing(member_id=member_id, amount=amount, active_status=True)

    _safe_add(session, bill)
    return bill

@staticmethod
def pay_bill(session, bill_id):
    try:
        bill = session.query(Billing).get(bill_id)
        bill.active_status = False
        session.commit()

    except Exception as e:
        session.rollback()