from sqlalchemy.orm.session import make_transient
from sqlalchemy import inspect
from datetime import datetime
from flask import abort
from .alchemy_base import AlchemyBase


db = AlchemyBase()


class BaseModel(db.Model):
    """
    Base model to add common columns, and provide some helper methods to make working with SQLAlchemy easier.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    time_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    time_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        super(BaseModel, self).__init__(**kwargs)

    @property
    def table_name(self):
        return self.__table__

    @property
    def is_new(self):
        """
        Check if an instance is new (does not have a DB record)
        :return: boolean, True if instance is a new record, False if instance is persisted
        """
        obj_state = inspect(self)
        return not (obj_state.persistent or obj_state.detached)

    @classmethod
    def create(cls, **kwargs):
        obj = cls(**kwargs)
        obj.save()
        return obj

    @property
    def is_persisted(self):
        """
        Check if an instance is persisted in the DB
        :return: boolean, True if instance is persisted in the DB, False if instance is a new record
        """
        return not self.is_new

    def is_a(self, model_name):
        """
        Method to test if a model is of a given type
        :param model_name: Name of the type of Model
        :type model_name: str
        :return: True if the instance is of the given type, False otherwise
        :rtype: bool
        """
        return isinstance(self, BaseModel) and type(self).__name__ == model_name

    def update(self, **attrs):
        """
        Set multiple attributes on model at once
        :param attrs: keyword args for any valid model property
        :return: self
        """
        for attr_name, attr in attrs.iteritems():
            self.__setattr__(attr_name, attr)
        self.save(defer_commit=True)
        return self

    def save(self, defer_commit=False):
        """
        Commit any changes to db
        Params
            :param defer_commit: boolean
        Return
            :return: self
        """
        db.session.add(self)
        if not defer_commit:
            db.session.commit()
        return self

    def delete(self, defer_commit=False):
        """
            Method to either Hard or Soft Delete a row.
            Params
                :param defer_commit: boolean
            Return
                :return: self
        """
        db.session.delete(self)
        if not defer_commit:
            db.session.commit()
            make_transient(self)
        return self

    @classmethod
    def count(cls, **lookup):
        """
        Method to get the number or objects in a result set
        Params
            :param lookup: kwargs
        Return
            :return: int
        """
        return cls._query(**lookup).count()

    @classmethod
    def _query(cls, order_by=None, **lookup):
        base_query = db.session.query(cls).filter_by(**lookup)

        if order_by is not None:
            base_query = base_query.order_by(order_by)

        return base_query

    @classmethod
    def find_all_by(cls, order_by=None, **lookup):
        """
        Method to find all of a Model by a given lookup
        Params
            :param order_by:
            :param lookup: kwargs
        Return
            :return: list
        """
        return cls._query(order_by, **lookup).all()

    @classmethod
    def find_one_by(cls, order_by=None, **lookup):
        """
        Method to find one of a Model by a given lookup
        Params
            :param order_by:
            :param lookup: kwargs
        Return
            :return: cls
        """
        return cls._query(order_by, **lookup).first()

    @staticmethod
    def commit():
        db.session.commit()

    @classmethod
    def get_or_abort(cls, pk, code=404):
        obj = cls.query.get(pk)
        if not obj:
            abort(code)
        return obj

    @classmethod
    def find_or_abort(cls, code_=404, **lookup):
        obj = cls.find_one_by(**lookup)
        if not obj:
            abort(code_)
        return obj

    @classmethod
    def get_unique(cls, add_to_session=False, **kwargs):
        """
            This class came from http://stackoverflow.com/a/24299429
                Add this mixin to any sqlalchemy model that needs uniqueness, for example facility addresses.
                use get_unique rather than the normal constructor to instantiate a new object.
                that will ensure that it will create a new object if no object has the passed in unique keys in the db.
                if an object already exists in the db with those unique keys, it returns that object instead.

            m1 = MyModel.get_unique(name='test')  # new instance
            m2 = MyModel.get_unique(name='test')  # from cache
            assert m1 is m2
            db.session.commit()  # inserts one row

            m1 = MyModel.get_unique(name='test')  # from database
            m2 = MyModel.get_unique(name='test')  # from cache
            assert m1 is m2

        """
        session = db.session
        # session.autoflush = False
        session._unique_cache = cache = getattr(session, '_unique_cache', {})
        key = (cls, tuple(kwargs.items()))
        o = cache.get(key)

        if o is None:
            o = session.query(cls).filter_by(**kwargs).first()

            if o is None:
                o = cls(**kwargs)
                if add_to_session:
                    db.session.add(o)

            cache[key] = o
        # session.autoflush = True
        return o
