from flask_script import Manager
from flask import current_app as app
from lib.ext.model.orm.base_model import db
from sqlalchemy_utils import database_exists, drop_database, create_database
from flask_migrate import stamp as alembic_stamp
import os
import yaml
from pydoc import locate

manager = Manager(usage="Perform Database actions")


@manager.command
def create():
    """
    Create database and all tables
    """
    if not database_exists(db.engine.url):
        app.logger.debug('Creating a fresh database to work with')
        create_database(db.engine.url)
        alembic_stamp()
        db.create_all()
    app.logger.debug('Database already exists, please drop the database and try again!')


@manager.command
def drop():
    """
    Drop the database if it exists
    :return:
    """
    app.logger.debug('Dropping the database!')
    if database_exists(db.engine.url):
        drop_database(db.engine.url)

    app.logger.error('Database does not exists!')


@manager.command
def seed():
    named_fixtures = {}
    for _file in sorted(os.listdir(app.config['SEEDS_PATH'])):
        if not _file.endswith(('yaml', 'yml')):
            continue
        with open(os.path.join(app.config['SEEDS_PATH'], _file), 'r') as f:
            print 'Loading fixtures from {}'.format(_file)
            yaml_doc = yaml.load(f)
            model_class = locate(yaml_doc['model'])
            if not model_class:
                raise RuntimeError('Unable to find model {} from yaml file {}'.format(yaml_doc['model'], _file))
            for fixture in yaml_doc['fixtures']:
                # print named_fixtures
                values = {}
                if isinstance(fixture, dict):
                    # this fixture has no name
                    fixture_data = fixture
                else:
                    # this fixture has a name
                    fixture_data = yaml_doc['fixtures'][fixture]

                for value_key in fixture_data:
                    value = fixture_data[value_key]
                    if isinstance(value, basestring) and value.startswith('~'):
                        values[value_key] = named_fixtures[value[1:]]
                    else:
                        values[value_key] = value
                instance = model_class(**values).save(defer_commit=True)
                if not isinstance(fixture, dict):
                    # store named fixture so other fixtures can reference is
                    named_fixtures[fixture] = instance

        db.session.commit()
