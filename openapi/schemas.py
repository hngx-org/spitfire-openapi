from pydantic import BaseModel, EmailStr, constr, validator


class RegisterSchema(BaseModel):
    email: EmailStr
    name: constr(to_lower=True, min_length=2, max_length=64)
    password: constr(min_length=8, max_length=64)
    confirm_password: constr(min_length=8, max_length=64)

    @validator("email")
    def valid_email_length(cls, v):
        if len(v) > 345:
            raise ValueError("Invalid email length")
        return v

    @validator("confirm_password")
    def check_confirm_password(cls, v, values, **kwargs):
        if v != values["password"]:
            raise ValueError("Passwords does not match")
        return v


class LoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)
