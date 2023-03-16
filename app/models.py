# encoding: utf-8
from datetime import datetime

from werkzeug.security import generate_password_hash

from app import db


class BaseModel:
    creat_time = db.Column(db.DateTime, default=datetime.now())
    update_time = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now())


# 管理员表


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(32), nullable=False, unique=True)  # 账号
    password = db.Column(db.String(64), nullable=False)  # 密码
    tags = db.relationship("Tag", backref="admin")  #


# 板块


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(10), nullable=False, unique=True)  # 标签名字
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 所属管理员
    # messages = db.relationship("Message", secondary="message_to_tag", backref="tags")  # 关系关联


# 分享


class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    content = db.Column(db.String(256), nullable=False)  # 内容
    create_time = db.Column(db.DateTime, default=datetime.now)  # 发布评论的时间
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))  # 所属用户
    tags = db.relationship(
        "Tag", secondary="message_to_tag", backref="messages")  # 关系关联


# 用户


class User(BaseModel, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    username = db.Column(db.String(32), nullable=False, unique=True)  # 账号
    nickname = db.Column(db.String(32), nullable=True, unique=True)  # 昵称
    password = db.Column(db.String(64), nullable=False)  # 密码
    logo_url = db.Column(db.String(64))
    messages = db.relationship("Message", backref="user")  # 关系关联

    def __init__(self, username, password, nickname, logo_url):
        self.username = username
        self.password = password
        self.nickname = nickname
        self.logo_url = logo_url


class MonitorData(db.Model):
    __tablename__ = "monitor_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    time = db.Column(db.DateTime, nullable=False, unique=True)
    hum_value = db.Column(db.Float, nullable=False)
    temp_value = db.Column(db.Float, nullable=False)

    def __init__(self, time, hum_value, temp_value):
        self.time = time
        self.hum_value = hum_value
        self.temp_value = temp_value


# 中间表


class MessageToTag(db.Model):
    __tablename__ = "message_to_tag"
    id = db.Column(db.Integer, primary_key=True)  # 主键
    message_id = db.Column(db.Integer, db.ForeignKey(
        "message.id", ondelete='CASCADE'))  # 所属评论
    tag_id = db.Column(db.Integer, db.ForeignKey(
        "tag.id", ondelete='CASCADE'))  # 所属标签
