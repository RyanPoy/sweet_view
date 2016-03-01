#coding: utf8
from __future__ import with_statement
from ..utils.decorates import classproperty
from ..query.criteria import Criteria
from mock.mock import self
from ..utils import *


class ActiveRecordMetaClass(type):
    
    def __init__(cls, name, bases, attr):
        model_instance = type.__init__(cls, name, bases, attr)
        if name != 'ActiveRecord':
            # set __table_name__ to Record Class
            if not hasattr(cls, '__table_name__'):
                table_name = pluralize_of(cls.__name__)
                setattr(cls, '__table_name__', camel_of(table_name))
            
            # id column must in columns validate
            if cls.__pk__ not in cls.__columns__:
                raise PKColumnNotInColumns()
            for c, err in [
                (cls.__pk__, PKColumnNotInColumns),
                (cls.__created_at__, CreatedAtColumnNotInColumns), 
                (cls.__updated_at__, UpdatedAtColumnNotInColumns),
                (cls.__created_on__, CreatedOnColumnNotInColumns),
                (cls.__updated_on__, UpdatedOnColumnNotInColumns),
            ]:
                if c and  c not in cls.__columns__:
                    raise err()

        return model_instance
    
    def __getattribute__(self, name):
        try:
            return type.__getattribute__(self, name)
        except AttributeError, _:
#             if FindMethodMissing.match(name):
#                 return FindMethodMissing(self, name)
            raise


class ActiveRecord(object):
    """
    A ORM. You can use it like this:
    - Query with chain 
        - where:
          User.where(name='pengyi').where('age != ?', 28).where('birthday between ? and ?', '1982-01-01', '1986-01-01')
         # => SELECT FROM users WHERE name = 'pengyi' AND age != 28 AND birthday between '1982-01-01' and '1986-01-01'
        
        - limit 
          User.where(name='pengyi').limit(10, 1) 
         # => SELECT FROM users WHERE name = 'pengyi' LIMIT 10 OFFSET 1
         
        - group/order/having ....
          User.where(name='pengyi').order('name DESC').group('name').having(age = 10)
         # => SELECT users.* FROM users WHERE `users`.`name` = 'pengyi' GROUP BY `users`.`name` HAVING `users`.`age` = 10 ORDER BY name DESC LIMIT 10 OFFSET 1
    
    - Query with method missing
      User.find_by_name('pengyi')
     # => SELECT FROM users WHERE name = 'pengyi'

      User.find_by_name_and_age('pengyi', 28)
     # => SELECT FROM users WHERE name = 'pengyi' AND age = 28
     
    - Create a record in database
      User.create(name = 'pengyi', age = 28)
     # => INSERT INTO users (name, age) VALUES ('pengyi', 28)
      
      User(name = 'pengyi', age = 28).save()
     # => INSERT INTO users (name, age) VALUES ('pengyi', 28)
     
    - Update
      u = User.find(1)  # 1 meams id
      u.update_attributes(name = 'poy', age = 30)
     # => UPDATE users SET name = 'poy', age = 30 WHERE id = 1
    
      User.where(age=20).update_all(name='poy', age='40)
     # => UPDATE users SET name = 'poy', age = 40 WHERE age = 20

    - Delete
      u = User.find(1)
      u.delete()
     # => DELETE FROM users WHERE id = 1
     
      u = User.where(age=20).delete_all()
     # => DELETE FROM users WHERE age = 20
    """
    __db__ = None
    __metaclass__ = ActiveRecordMetaClass
    __columns__ = set([])
    __pk__ = 'id'
    __created_at__ = 'created_at'
    __updated_at__ = 'updated_at'
    __created_on__ = None
    __updated_on__ = None

    def __init__(self, dict_args={}, **kwargs):
        self.__dict__.update(dict_args)
        self.__dict__.update(kwargs)
        self.__is_persisted = False
        self.__origin_attrs = {}

    def _get_origin(self, attr):
        return self.__origin_attrs.get(attr)
    
    def is_dirty(self, *attrs):
        dirty_attrs = {}
        for k, v in self.__origin_attrs.iteritems():
            dirty_v = getattr(self, k, v) 
            if dirty_v != v:
                dirty_attrs[k] = (dirty_v, v)
        if not dirty_attrs:
            return False
        for a in attrs:
            if a not in dirty_attrs:
                return False
        return True

    @property
    def is_persisted(self):
        return self.__is_persisted
    
    def _sync_attrs(self):
        for col in self.__columns__:
            self.__origin_attrs[col] = getattr(self, col, None)
        return self
    
    def __getattr__(self, name):
        try:
            return super(ActiveRecord, self).__getattribute__(name)
        except AttributeError, _:
            if name in self.__columns__:
                return None
#             association = self.association_of(name)
#             if association:
#                 if association.is_belongs_to():
#                     # A belongs_to B
#                     # A.B  => "SEELCT B.* FROM B WHERE id = A.B_id"
#                     return association.target.find(getattr(self, association.foreign_key))
#                 elif association.is_has_one():
#                     # A has_one B
#                     # A.B => "SELECT B.* FROM B WHERE A_id = A.id"
#                     return association.target.where(**{association.foreign_key: self.id}).first
#                 elif association.is_has_many():
#                     # A has_many B through C
#                     if association.through:
#                         # A.bs  => "SELECT B.* FROM B INNER JOIN C ON C.b_id = B.id AND C.a_id = A.id"
#                         through_association = self.association_of(association.through)
#                         if through_association.is_has_many():
#                             # fk_value={}, has_and_belongs_to_many_association=None):
#                             return HasManyCollection(association.target, fk_value={through_association.foreign_key: self.id}) \
#                                         .joins(association.through) \
#                                         .where('%s.%s = %s' % (association.through, through_association.foreign_key, self.id))
#                     else:
#                         # A has_many B
#                         # A.bs => "SELECT B.* FROM B WHERE A_id = A.id"
#                         return HasManyCollection(association.target, fk_value={association.foreign_key: self.id}).where(**{association.foreign_key: self.id})
#                 else: # has_and_belongs_to_many
#                     join_str = 'INNER JOIN %s ON %s.%s = %s.id' % (association.join_table, association.join_table, association.association_foreign_key, association.target.table_name)
#                     # return association.target.joins(join_str).where('%s.%s = %s' % (association.join_table, association.foreign_key, self.id)
#                     return HasAndBelongsToManyCollection(association.target, fk_value={association.foreign_key: self.id}) \
#                                         .joins(join_str).where('%s.%s = %s' % (association.join_table, association.foreign_key, self.id))
#             if CreateOrBuildMethodMissing.match(name):
#                 return CreateOrBuildMethodMissing(self, name)
            raise

    @classproperty
    def table_name(cls):
        return cls.__table_name__

    def persist_attrs(self, contains_id=False):
        relt = dict([ (c, getattr(self, c, None)) for c in self.__columns__ ])
        if not contains_id:
            relt.pop(self.__pk__)
        return relt

#     @classproperty
#     def association_dict(cls):
#         if not hasattr(cls, '__association_dict__'):
#             cls.__association_dict__ = {}
#         return cls.__association_dict__
# 
#     @classmethod
#     def association_of(cls, name):
#         return cls.association_dict.get(name, None)
#     
#     @classproperty
#     def validate_func_dict(cls):
#         if not hasattr(cls, '__validates_dict__'):
#             cls.__validates_dict__ = {}
#         return cls.__validates_dict__
# 
#     @classproperty
#     def all(cls):
#         """ find all records
#         @return a record array
#         eg.
#             User.all
#             User.where(age=10).all
#         """
#         return Collection(cls).all
#     
#     @classproperty
#     def first(cls):
#         """ find the first record
#         @return a record
#         eg.
#             User.first
#             User.where(age=10).first
#         """
#         return Collection(cls).first
#     
#     @classproperty
#     def last(cls):
#         """ find the last record
#         @return a record
#         eg.
#             User.last
#             User.where(age=10).last
#         """
#         return Collection(cls).last
# 
#     @classmethod
#     def select(cls, *args):
#         return Collection(cls).select(*args)
# 
#     
#     @classmethod
#     def where(cls, *args, **kwargs):
#         """ condition query
#         eg.
#             User.where(username="abc").where(password="123")
#             User.where("username='abc' and password='123'")
#             User.where("username=? and password=?", 'abc', '123')
#         """
#         return Collection(cls).where(*args, **kwargs)
# 
#     @classmethod
#     def find(cls, *ids):
#         """ find record by ids
#         @return:    if there is a id and found it will return a record
#                     if there are many ids and found them will return a record array
#                     if any id not found, throw RecordNotFound exception
#         """
#         return Collection(cls).find(*ids)
# 
#     @classmethod
#     def limit(cls, limit=0, offset=0):
#         """ limit query
#         eg. 
#             User.limit(10)
#             User.limit(10, 1)
#         """
#         return Collection(cls).limit(limit, offset)
# 
#     @classmethod
#     def count(cls):
#         """ get count number
#         @return a number
#         eg. 
#             User.count()
#             User.where('username=123').count()
#         """
#         return Collection(cls).count()
#     
#     @classmethod
#     def sum(cls, attribute_name):
#         """ get sum number
#         @return number
#         eg.
#             User.sum(age)
#             User.where(username=123).sum()
#         """
#         return Collection(cls).sum(attribute_name)
# 
#     @classmethod
#     def order(cls, *args):
#         """ order query
#         eg.
#             User.order('age')
#             User.order('age ASC')
#             User.order('age DESC')
#         """
#         if args:
#             return Collection(cls).order(args[0]) 
#         return Collection(cls)
# 
#     @classmethod
#     def group(cls, group):
#         """ group query
#         eg. 
#             User.group('username')
#         """
#         return Collection(cls).group(group)
# 
#     @classmethod
#     def having(cls, *args, **kwargs):
#         """ having query when group
#         Note: if there is not use group, the having will be not useful
#         eg.
#             User.group('username').having(age=1)
#         """
#         return Collection(cls).having(*args, **kwargs)
# 
#     @classmethod
#     def joins(cls, *joins):
#         """
#         Joining a Single Association
#             Category.joins('posts')
#         # => SELECT categories.* FROM categories
#                INNER JOIN posts ON posts.category_id = categories.id
# 
#         Joining Multiple Associations
#             Post.joins('category', 'comments')
#         # => SELECT posts.* FROM posts
#                INNER JOIN categories ON posts.category_id = categories.id
#                INNER JOIN comments ON comments.post_id = posts.id
#         
#         Joining Nested Associations (Single Level)
#             Post.joins({'comments': 'guest'})
#         # => SELECT posts.* FROM posts
#                INNER JOIN comments ON comments.post_id = posts.id
#                INNER JOIN guests ON guests.comment_id = comments.id
# 
#         Joining Nested Associations (Multiple Level)
#             Category.joins({ 'posts': [{'comments': 'guest'}, 'tags'])
#         # => SELECT categories.* FROM categories
#                INNER JOIN posts ON posts.category_id = categories.id
#                INNER JOIN comments ON comments.post_id = posts.id
#                INNER JOIN guests ON guests.comment_id = comments.id
#                INNER JOIN tags ON tags.post_id = posts.id
#         """
#         return Collection(cls).joins(*joins)
#     
#     def valid(self):
#         return True
    
    def _get_attr(self, attrname, default=None):
        return getattr(self, attrname, default)

    @classmethod
    def create(cls, attr_dict={}, **attributes):
        """ persist a active record. 
        @return：record instance if successful, else return None. 
                it will throw exception when any exception occur
        eg. 
            User.create(username='abc', password='123')
        """
        record = cls(attr_dict, **attributes)
        return record if record.save() else None
    
    def  _prepare_at_or_on(self, attrs_dict):
        def _build_at_or_on(at_or_on_attrname, attrs_dict, is_at=True):
            str_2_datetime_or_date = str2datetime if is_at else str2date
            cur_datetime_or_date = datetime.now if is_at else datetime.today
            if at_or_on_attrname:
                value = attrs_dict.get(at_or_on_attrname, None) or self._get_attr(at_or_on_attrname)
                value = str_2_datetime_or_date(value)
                if value is None:
                    value = cur_datetime_or_date() 
                setattr(self, at_or_on_attrname, value)
                attrs_dict[at_or_on_attrname] = self._get_attr(at_or_on_attrname)
        for at in (self.__created_at__, self.__updated_at__):
            _build_at_or_on(at, attrs_dict)
        for on in (self.__created_on__, self.__updated_on__):
            _build_at_or_on(on, attrs_dict, False)
        return self

    def save(self):
        """ persist a record instance.
        @return：record instace if successful, else return None. 
                it will throw exception when any exception occur
        eg.
            u = User(username="abc", password="123456").save()
        """
        criteria = self._new_criteria()
        if self.is_persisted: # update
            attrs = self.persist_attrs()
            self._prepare_at_or_on(attrs)
            criteria.where(id=self.pk).update(**attrs)
        else: # insert
            attrs = self.persist_attrs()
            self._prepare_at_or_on(attrs)
            setattr(self, self.__pk__, criteria.insert(**attrs))
            self.__is_persisted = True
        self._sync_attrs()
        return self

    @classmethod
    def _new_criteria(cls):
        return Criteria().from_(cls.table_name)

#     def relate(self, *models):
#         Collection(self.__class__).save(self)
#         return self

    def update_attributes(self, **attributes):
        """ update attributes
        eg. 
            u = User(username="abc", password="123").save().update_attributes(username="efg", password="456")
        return: self if update successful else False
        """
        if not self.is_persisted:
            raise RecordHasNotBeenPersisted()
        self._prepare_at_or_on(attributes)
        criteria = self._new_criteria().where(id=self.pk)
        criteria.update(attributes)

        for name, value in attributes.iteritems():
            setattr(self, name, value)
        return self

    @classmethod
    def update_all(cls, **attributes):
        cls._new_criteria().update(**attributes)
        return True

    @property
    def pk(self):
        return self.id

#     def delete(self):
#         """delete a record instance.
#         eg.
#             u = User.find(1)
#             u.delete()
#         """
#         # @TODO: 需要按照关系再次删除相关的数据
#         return self.where(id=self.id).delete_all()
# 
#     @classmethod
#     def delete_all(cls):
#         """ delete all records
#         eg.
#             User.delete_all()
#             User.find(1, 2, 3).delete_all()
#         """
#         Collection(cls).delete_all()
#         return True
# 
#     @classmethod
#     def _get_db(cls):
#         if cls.__db__ is None:
#             cls.__db__ = pyrails.get_database()
#         return cls.__db__
#     
#     @property
#     def is_persisted(self):
#         """ check an record had been persisted
#         """
#         # @TODO: fix me ! 
#         #       the check method is so simple.
#         #       should check it which is query from db
#         return self.id is not None
# 
#     @classproperty
#     @contextmanager
#     def transaction(cls):
#         try:
#             db = cls._get_db()
#             db.set_autocommit(False)
#             yield None
#             db.commit()
#         except ValidationError:
#             db.rollback()
#         except:
#             db.rollback()
#             raise
#         finally:
#             try:
#                 db.set_autocommit(True)
#             except:
#                 pass
# 
#     def add_error(self, attr_name, msg):
#         self.errors.setdefault(attr_name, []).append(msg)
#         return self
# 
#     def validate(self, on='save'):
#         return all([ valid(record=self) for valid in self.__class__.validate_func_dict.get(on, {}) ])
# 
    def to_dict(self):
        d = dict([ (c, getattr(self, c)) for c in self.__columns__ ])
        self._prepare_at_or_on(d)
        return d
