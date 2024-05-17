import enum

from sqlalchemy import Boolean, Column, Integer, String, func, Table, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


image_m2m_tag = Table(
    "image_m2m_tag",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("image_id", Integer, ForeignKey("images.id", ondelete="CASCADE")),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE")),
)


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    image = Column(String(255), nullable=False)
    edited_image = Column(String(255), nullable=False)
    description = Column(String(100), nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    user = relationship('User', backref="images", lazy="joined")
    comments = relationship('Comment', backref="images")
    tags = relationship("Tag", secondary=image_m2m_tag, backref="images", passive_deletes=True)
    qr_code = Column(String(255), nullable=False)


class Role(enum.Enum):
    admin: str = "admin"
    moderator: str = "moderator"
    user: str = "user"


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user, nullable=True)
    refresh_token = Column(String(255), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=False)
    confirmed = Column(Boolean, default=False)


class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String(25), nullable=False, unique=True)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    comment = Column(String(255), nullable=False)
    user_id = Column('user_id', ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    user = relationship('User', backref="comments", lazy="joined")
    image_id = Column('image_id', ForeignKey('images.id', ondelete='CASCADE'), nullable=True)
    created_at = Column('created_at', DateTime, default=func.now())
    updated_at = Column('updated_at', DateTime, default=func.now(), onupdate=func.now())