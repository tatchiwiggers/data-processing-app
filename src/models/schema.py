from pydantic import BaseModel, EmailStr


class WebDriverConfig(BaseModel):
    driver_path: str
    headless: bool = False


class ProductData(BaseModel):
    product_link: str
    product_image: str
    product_title: str
    previous_price: str
    current_price: str
    discount: str
    installments: str
    seller: str


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
