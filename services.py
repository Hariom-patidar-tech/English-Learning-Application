import random
from datetime import datetime, timedelta
from jose import jwt
from config import settings
from models import OTP, User,Question
import json

#  Generate OTP
def generate_otp():
    return str(random.randint(1000, 9999))


# 📲 Create OTP
def create_otp(db, phone):
    otp_code = generate_otp()

    otp = OTP(
        phone_number=phone,
        otp_code=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
        is_used=False
    )

    db.add(otp)
    db.commit()

    return otp_code


# ✅ Verify OTP
def verify_otp(db, phone, otp_code):
    otp = db.query(OTP).filter(
        OTP.phone_number == phone,
        OTP.otp_code == otp_code,
        OTP.is_used == False
    ).first()

    if not otp:
        return False

    if otp.expires_at < datetime.utcnow():
        return False

    otp.is_used = True
    db.commit()

    return True


# 👤 Get User
def get_user(db, phone):
    return db.query(User).filter(User.phone_number == phone).first()


# 👤 Create User
def create_user(db, phone, name=None, email=None):
    user = User(
        phone_number=phone,
        name=name,
        email=email,
        is_verified=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# 🔐 Create JWT Token
def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


from models import TempUser


def save_temp_user(db, phone_number, name, email):
    
    existing = db.query(TempUser).filter(
        TempUser.phone_number == phone_number
    ).first()

    if existing:
        db.delete(existing)
        db.commit()

    temp = TempUser(
        phone_number=phone_number,
        name=name,
        email=email
    )

    db.add(temp)
    db.commit()
    db.refresh(temp)
    return temp


def get_temp_user(db, phone_number):
    return db.query(TempUser).filter(
        TempUser.phone_number == phone_number
    ).first()


def delete_temp_user(db, phone_number):
    temp = db.query(TempUser).filter(
        TempUser.phone_number == phone_number
    ).first()

    if temp:
        db.delete(temp)
        db.commit()



import json
from models import Question

from difflib import SequenceMatcher

def check_answer(user_answer, correct_answer):
    ratio = SequenceMatcher(
        None,
        user_answer.lower(),
        correct_answer.lower()
    ).ratio()

    return ratio > 0.7


def save_questions(db, groq_output):

    if isinstance(groq_output, dict):
        data = [groq_output]
    elif isinstance(groq_output, list):
        data = groq_output
    else:
        data = json.loads(groq_output)

    for item in data:
        question_text = item.get("question", "").lower()

        # 🔥 nan filter
        if not question_text or "nan" in question_text:
            continue

        db.add(Question(
            question=item.get("question"),
            correct_answer=item.get("answer"),
            hint1=item.get("hint1"),
            hint2=item.get("hint2"),
            topic=item.get("topic", "general"),
            difficulty=item.get("difficulty", "easy")
        ))

    db.commit()