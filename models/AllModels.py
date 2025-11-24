from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Float, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

def get_base():
    return Base

class Member(Base):
    __tablename__ = 'member'

    member_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)

    health_metrics = relationship("HealthMetrics", back_populates="member")
    goals = relationship("Goal", back_populates="member")
    training_sessions = relationship("TrainingSession", back_populates="member")
    bills = relationship("Billing", back_populates="member")

class Trainer(Base):
    __tablename__ = 'trainer'

    trainer_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)

    training_sessions = relationship("TrainingSession", back_populates="trainer")
    group_sessions = relationship("GroupTrainingSession", back_populates="trainer")

class Admin(Base):
    __tablename__ = 'admin'
    
    admin_id = Column(Integer, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    billing = relationship("Billing", back_populates="admin")
    training_sessions = relationship("TrainingSession", back_populates="admin")
    group_sessions = relationship("GroupTrainingSession", back_populates="admin")
    room_bookings = relationship("RoomBooking", back_populates="admin")

class HealthMetrics(Base):
    __tablename__ = 'health_metrics'

    metric_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member.member_id'))

    height_cm = Column(Integer)
    mass_kg = Column(Float)
    heart_rate = Column(Integer)
    date_taken = Column(DateTime, nullable=False) 

    member = relationship("Member", back_populates="health_metrics")

class Goal(Base):
    __tablename__ = 'goal'

    goal_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member.member_id'))

    target_mass_kg = Column(Float)
    target_bf_percentage = Column(Float)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)

    member = relationship("Member", back_populates="goals")

class TrainingSession(Base):
    __tablename__ = 'training_session'

    session_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room_booking.room_id'))
    member_id = Column(Integer, ForeignKey('member.member_id'))
    trainer_id = Column(Integer, ForeignKey('trainer.trainer_id'))
    admin_id = Column(Integer, ForeignKey('admin.admin_id'))

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)

    member = relationship("Member", back_populates="training_sessions")
    trainer = relationship("Trainer", back_populates="training_sessions")
    admin = relationship("Admin", back_populates="training_sessions")
    room = relationship("RoomBooking", back_populates="training_sessions")

Index('idx_start_time', TrainingSession.start_time)
Index('ix_trainer_start_end', TrainingSession.trainer_id, TrainingSession.start_time, TrainingSession.end_time)

class GroupTrainingSession(Base):
    __tablename__ = 'group_training_session'

    session_id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room_booking.room_id'))
    trainer_id = Column(Integer, ForeignKey('trainer.trainer_id'))
    admin_id = Column(Integer, ForeignKey('admin.admin_id'))

    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    num_participants = Column(Integer, nullable=False)

    trainer = relationship("Trainer", back_populates="group_sessions")
    admin = relationship("Admin", back_populates="group_sessions")
    room = relationship("RoomBooking", back_populates="group_sessions")

Index('idx_start_time_group', GroupTrainingSession.start_time)

class RoomBooking(Base):
    __tablename__ = 'room_booking'

    room_id = Column(Integer, primary_key=True)
    used_status = Column(Boolean, nullable=False)

    admin = relationship("Admin", back_populates="room_bookings")
    training_sessions = relationship("TrainingSession", back_populates="room")
    group_sessions = relationship("GroupTrainingSession", back_populates="room")

class Billing(Base):
    __tablename__ = 'billing'

    bill_id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey('member.member_id'))
    admin_id = Column(Integer, ForeignKey('admin.admin_id'))

    amount = Column(Float, nullable=False)
    active_status = Column(Boolean, nullable=False)

    member = relationship("Member", back_populates="bills")
    admin = relationship("Admin", back_populates="billing")