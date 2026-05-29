from pydantic import BaseModel, field_validator
import re  

# 🔹 SEND OTP
class SendOTP(BaseModel):
    phone_number: str

    @field_validator("phone_number")
    def validate_phone(cls, v):
        pattern = r"^\+\d{10,15}$"
        if not re.match(pattern, v):
            raise ValueError("Phone number must include country code (e.g. +919876543210)")
        return v


# 🔹 VERIFY OTP (LOGIN ONLY)
class VerifyOTP(BaseModel):
    phone_number: str
    otp: str


class Signup(BaseModel):
    phone_number: str
    name: str | None = None
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone_number: str

    class Config:
        from_attributes = True


class VerifySignup(BaseModel):
    phone_number: str
    otp: str


class ScriptCreate(BaseModel):
    title: str
    category: str
    difficulty: str
    frequency: str
    steps: list[str]