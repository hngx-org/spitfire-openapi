from pydantic import BaseModel, EmailStr, constr, validator


class RegisterSchema(BaseModel):
    email: EmailStr
    name: constr(regex=r'^[a-zA-Z0-9_]+$',to_lower=True, min_length=2, max_length=64)
    password: constr(min_length=8, max_length=64)
    confirm_password: str

    @validator("email")
    def valid_email_length(cls, email):
        if len(email) > 345:
            raise ValueError("Invalid email length")
        return email
    

    @validator("confirm_password")
    def passwords_are_same(cls, confirm_password,values, **kwargs):
        if "password" in values and confirm_password != values["password"]:
            raise ValueError("Passwords do not match")
        return confirm_password


class LoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=8, max_length=64)



class CreatePaymentSchema(BaseModel):
    paymentToken : constr(min_length=4, max_length=21) 
    @validator("paymentToken")
    def validate_token(cls, paymentToken):
        if paymentToken != "examplepaymenttoken":
            raise ValueError("Invalid Payment Token")
        return paymentToken
