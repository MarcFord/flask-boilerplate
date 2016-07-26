import uuid
from flask_sqlalchemy import SQLAlchemy, Model, _BoundDeclarativeMeta, _QueryProperty
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base


class AlchemyBase(SQLAlchemy):
    """
    Configure SQLAlchemy Declarative Base.
    """
    def __init__(self):
        super(AlchemyBase, self).__init__()

        def fk_fixed_width(constraint, table):
            str_tokens = [table.name] +\
                         [element.parent.name for element in constraint.elements] +\
                         [element.target_fullname for element in constraint.elements]
            guid = uuid.uuid5(uuid.NAMESPACE_OID, "_".join(str_tokens).encode('ascii'))
            return str(guid)

        convention = {
            "fk_fixed_width": fk_fixed_width,
            "ix": 'ix_%(column_0_label)s',
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(column_0_name)s",
            "fk": "fk_%(fk_fixed_width)s",
            "pk": "pk_%(table_name)s"
        }
        metadata = MetaData(naming_convention=convention)
        self.Model = declarative_base(metadata=metadata, cls=Model, name='Model', metaclass=_BoundDeclarativeMeta)
        self.Model.query = _QueryProperty(self)
