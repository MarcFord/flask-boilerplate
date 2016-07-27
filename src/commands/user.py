from flask_script import prompt, prompt_pass, Option
from lib.ext.command.base_command import BaseCommand
from models.user import User
from models.role import Role, UserRole
from flask import current_app as app
from app import db
from flask_security.utils import encrypt_password


class UserCreate(BaseCommand):
    """Create a New User"""
    def run(self):
        email = prompt('Email Address')
        password = prompt_pass('Password')
        if password == prompt_pass('Confirm Password'):
            user = app.user_datastore.create_user(email=email, password=encrypt_password(password))
            app.user_datastore.activate_user(user)
            db.session.commit()
            self.stdout.write('New User Created, <{id} : {email}>'.format(id=user.id, email=user.email))
        else:
            self.stderr.write('Passwords did not match!')


class RoleCreate(BaseCommand):
    """Create a New Role"""
    def run(self):
        name = prompt('Role Name')
        desc = prompt('Role Description')
        role = Role(name=name, description=desc).save()
        self.stdout.write(
            'New Role Created, <{id} : {name} : {desc}>'.format(
                id=role.id,
                name=role.name,
                desc=role.description
            )
        )


class RoleList(BaseCommand):
    """List Roles in System"""
    def run(self):
        roles = Role.find_all_by()
        self.stdout.write('Roles in System:')
        self.stdout.write("NAME\t\t\tDESCRIPTION")
        self.stdout.write("-------------\t\t-------------")
        for role in roles:
            self.stdout.write("{name}\t\t{desc}".format(name=role.name, desc=role.description))


class RoleAssign(BaseCommand):
    """Assign Role to User"""
    option_list = (
        Option('--email', '-e', dest='email'),
        Option('--role', '-r', dest='role'),
    )

    def run(self, email, role):
        user = User.find_one_by(email=email)
        role_obj = Role.find_one_by(name=role)
        if user and role:
            UserRole(user=user, role=role_obj).save()
            self.stdout.write('User, {email}, now has role, {role_name}'.format(email=user.email, role_name=role_obj.name))
        else:
            self.stderr.write('Unable to find either user or role!')

