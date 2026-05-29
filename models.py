from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime
from db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), unique=True, index=True)
    name = Column(String(100))
    email = Column(String(100))
    is_verified = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class TempUser(Base):
    __tablename__ = "temp_users"

    id = Column(Integer, primary_key=True, index=True)
    phone_number = Column(String(20), unique=True, index=True)
    name = Column(String(100))
    email = Column(String(100))


class OTP(Base):
    __tablename__ = "otps"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String(20), index=True)
    otp_code = Column(String(10))
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Script(Base):
    __tablename__ = "scripts"

    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    category = Column(String(100))
    difficulty = Column(String(50))
    frequency = Column(String(50))
    user_id = Column(Integer, ForeignKey("users.id"))


class ScriptStep(Base):
    __tablename__ = "script_steps"

    id = Column(Integer, primary_key=True)
    step_text = Column(String(500))
    is_completed = Column(Boolean, default=False)
    script_id = Column(Integer, ForeignKey("scripts.id"))


class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    script_id = Column(Integer)
    action = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    question = Column(String(500))
    correct_answer = Column(String(100))
    hint1 = Column(String(200))
    hint2 = Column(String(200))

    topic = Column(String(100))          # ✅ ADD
    difficulty = Column(String(50))      # ✅ ADD


class UserQuiz(Base):
    __tablename__ = "user_quiz"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    current_question_id = Column(Integer, ForeignKey("questions.id"))
    score = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
class Attempt(Base):
    __tablename__ = "attempts"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=True)
    question_id = Column(Integer)
    attempt_count = Column(Integer, default=1)