#!/usr/bin/env python
import urllib

from flask_script import Manager
from flask_script.commands import Clean, Server, Shell
from app import ApplicationFactory
from flask_migrate import MigrateCommand
from commands.orm import manager as orm_commands
from commands.assets import Build, Watch, LintJS
from commands.user import UserCreate, RoleCreate, RoleAssign, RoleList


manager = Manager(ApplicationFactory.create_application)

manager.add_option('-e', '--env', dest='env', required=False, default='development')


manager.add_command("server", Server())
manager.add_command("shell", Shell())
manager.add_command('clean', Clean())
manager.add_command('db', MigrateCommand)
manager.add_command('orm', orm_commands)
manager.add_command('build', Build())
manager.add_command('watch', Watch())
manager.add_command('lint_js', LintJS())
manager.add_command('create_user', UserCreate())
manager.add_command('create_role', RoleCreate())
manager.add_command('assign_role', RoleAssign())
manager.add_command('list_roles', RoleList())


@manager.command
def routes():
    """
    Print all routes
    """
    print('\n'.join(sorted(map(lambda rule: urllib.unquote("{:50s} {:30s} {}".format(rule.endpoint, ','.join(rule.methods), rule)), manager.app.url_map.iter_rules()))))


if __name__ == '__main__':
    manager.run()
