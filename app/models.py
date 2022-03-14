# Create Table Models for database

from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey, JSON
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Device(Base):
    __tablename__ = "devices"

    device_id = Column(String, nullable=False, unique=True)
    device_name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)
    sensor_type = Column(String, nullable=False)
    active = Column(Boolean, nullable=True, server_default="FALSE")
    location = Column(String, nullable=True, server_default="My Location")
    description = Column(String, nullable=False)
    developer_id = Column(
        String,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    id = Column(Integer, primary_key=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class Users(Base):
    __tablename__ = "users"

    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_id = Column(String, nullable=False, unique=True)
    api_key = Column(String, nullable=True, unique=True)
    id = Column(Integer, nullable=False, primary_key=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )


class Data(Base):
    __tablename__ = "data"

    id = Column(Integer, primary_key=True, nullable=False)
    device_id = Column(
        String,
        ForeignKey("devices.device_id", ondelete="CASCADE"),
        nullable=False,
    )
    data = Column(JSON, nullable=False)
    stream_id = Column(String, nullable=False, unique=True)
    developer_id = Column(
        String,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=True, server_default=text("now()")
    )
