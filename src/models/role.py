from lib.ext.model.orm import BaseModel, db
from flask_security import RoleMixin
from sqlalchemy.orm import relationship
from sqlalchemy import UniqueConstraint


class Role(BaseModel, RoleMixin):
    __tablename__ = 'Roles'
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class UserRole(BaseModel):
    __tablename__ = 'UserRoles'
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id', name='unique_role_user_user_roles'),
    )
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = relationship('User', uselist=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))
    role = relationship('Role', uselist=False)
