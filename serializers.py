from pydantic import BaseModel, EmailStr


class UserValidatorUser(BaseModel):
    username: str


class UserValidatorEmail(BaseModel):
    email: EmailStr


class UserValidatorPass(BaseModel):
    password: str


class UserValidator(UserValidatorPass):
    username: str
    email: EmailStr


class ArticleValidatorTitle(BaseModel):
    title: str


class ArticleValidatorText(BaseModel):
    text: str


class ArticleValidatorUser(BaseModel):
    user_id: int


class ArticleValidator(ArticleValidatorUser):
    title: str
    text: str
