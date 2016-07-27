from flask_script import prompt, prompt_pass, Option
from lib.ext.command.base_command import BaseCommand
from models.user import User
from models.role import Role, UserRole
from app import security


class UserCreate(BaseCommand):
    """Create a New User"""
    def run(self):
        email = prompt('Email Address')
        password = prompt_pass('Password')
        if password == prompt_pass('Confirm Password'):
            user = security.datastore.create_user(email=email, password=password)
            security.datastore.activate_user(user)
            self.logger.info('New User Created, <{id} : {email}>'.format(id=user.id, email=user.email))
        else:
            self.logger.error('Passwords did not match!')


class RoleCreate(BaseCommand):
    """Create a New Role"""
    def run(self):
        name = prompt('Role Name')
        desc = prompt_pass('Role Description')
        role = Role(name=name, description=desc).save()
        self.logger.info(
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
        self.logger.info('Roles in System:')
        for role in roles:
            self.logger.info("Name: {name}\t\tDescription: {desc}".format(name=role.name, desc=role.description))


class RoleAssign(BaseCommand):
    """Assign Role to User"""
    option_list = (
        Option('--email', '-e', dest='email'),
        Option('--role', '-r', dest='role'),
    )

    def run(self, email, role):
        user = User.find_one_by(email=email)
        role = Role.find_one_by(name=role)
        if user and role:
            security.datastore.add_role_to_user(user=user, role=role)
            self.logger.info('User, {email}, now has role, {role_name}'.format(email=user.email, role_name=role.name))
        else:
            self.logger.error('Unable to find either user or role!')

