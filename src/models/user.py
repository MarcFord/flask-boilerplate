from lib.ext.model.orm import BaseModel, db
from sqlalchemy.orm import relationship
from flask_security import UserMixin


class User(BaseModel, UserMixin):
    __tablename__ = 'Users'
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = relationship('Role', secondary='UserRoles', backref=db.backref('users', lazy='dynamic'))
    last_login_at = db.Column(db.DateTime, nullable=True)
    current_login_at = db.Column(db.DateTime, nullable=True)
    current_login_ip = db.Column(db.String(128))
    login_count = db.Column(db.Integer)
