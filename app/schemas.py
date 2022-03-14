# define structure of what to be sent and received

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.database import Base


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    user_id: str


class User(BaseModel):
    email: EmailStr
    user_id: str
    created_at: datetime
    api_key: str

    class Config:
        orm_mode = True


class DeviceBase(BaseModel):
    device_id: str
    description: str
    active: bool
    device_name: str
    device_type: str
    sensor_type: str
    location: str


class DeviceCreate(DeviceBase):
    pass


class Device(DeviceBase):
    created_at: datetime
    developer_id: str

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    id: Optional[str] = None


class DataStream(BaseModel):
    stream_id: str
    device_id: str
    developer_id: str
    data: dict
    created_at: datetime

    class Config:
        orm_mode = True


class DataStreamCreate(BaseModel):
    device_id: str
    data: dict
