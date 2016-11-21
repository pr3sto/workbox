from ming import schema
from ming.odm import MappedClass
from ming.odm import FieldProperty, ForeignIdProperty
from hellomongo.model import DBSession
   
class container(MappedClass):
    class __mongometa__:
        session = DBSession
        name = 'container'

    _id = FieldProperty(schema.ObjectId)
    container_id = FieldProperty(schema.String(required = True))
    status = FieldProperty(schema.String(if_missing = ''))
    author_user_id = FieldProperty(schema.Int(if_missing = -1))
