from lib.ext.model.orm import BaseModel, db
from flask_security import RoleMixin
from sqlalchemy.orm import relationship


class Role(BaseModel, RoleMixin):
    __tablename__ = 'Roles'
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class UserRole(BaseModel):
    __tablename__ = 'UserRoles'
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    user = relationship('User', back_populates='user_roles', uselist=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Roles.id'))
    role = relationship('Role', back_populates='user_roles', uselist=False)
