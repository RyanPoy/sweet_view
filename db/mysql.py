#coding: utf8
from itertools import izip
from pyrails.schema import Table, Column
from pyrails.support import is_str, is_datetime, is_date, flatten, str2date, str2datetime
import MySQLdb
import time
import itertools


class Adapter(object):

    def __init__(self, database, user='root', password='', host='localhost', port=3306, charset='utf8', show_sql=False):
        self._db_args = dict(db=database, user=user, passwd=password, host=host, port=port, charset=charset,
                             init_command='SET time_zone = "+0:00"', sql_mode="TRADITIONAL", use_unicode=True)
        self._conn = None
        self.show_sql = show_sql
        self._reconnect()

    def fetchone(self, sql, params=[]):
        """Returns the first row returned for the given query."""
        rows = self.fetchall(sql, params)
        return rows[0] if rows else None
    
    def fetchall(self, sql, params=[]):
        """Returns a row list for the given query and parameters."""
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, params)
            column_names = [d[0] for d in cursor.description]
            return [ dict(itertools.izip(column_names, row)) for row in cursor ]
        finally:
            cursor.close()
            
        return self._execute(sql, params).cursor.fetchall()

    def execute_lastrowid(self, sql, params=[]):
        """Executes the given query, returning the lastrowid from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, params)
            return cursor.lastrowid
        finally:
            cursor.close()
    
    def execute_rowcount(self, sql, params = []):
        """Executes the given query, returning the rowcount from the query."""
        cursor = self._cursor()
        try:
            self._execute(cursor, sql, params)
            return cursor.rowcount
        finally:
            cursor.close()
            
    def _execute(self, cursor, sql, params=[]):
        btime = time.time()
        raw_sql = ''
        if self.show_sql:
            raw_sql = self.__show_sql(sql, params)
        sql = sql.replace('?', '%s') # @TODO: should fix a bug if query like this: select users.* from users where users.name like "?abc"
        cursor.execute(sql, params)
        if self.show_sql:
            print '##', raw_sql, (time.time() - btime)
        return self
    
    def get_table_by(self, name):
        sql = 'SHOW FULL COLUMNS FROM %s' % name
        table = Table(name)
        for field in self.fetchall(sql):
            table.add_column(Column(
                name=field['Field'], type=self.column_type_of(field['Type']), null=field['Null'] == "YES", default=field['Default']
#                field['Collation']
            ))
        return table
    
    def column_type_of(self, db_field_type):
        db_field_type = db_field_type.lower().strip().split('(')[0]
        for field_type, column_type in { 
            'varchar': Column.Type.string, 'text': Column.Type.text, 'tinyint': Column.Type.boolean, 
            'float': Column.Type.float, 'decimal': Column.Type.decimal, 'datetime': Column.Type.datetime, 
            'date': Column.Type.date, 'timestamp': Column.Type.timestamp, 'blob': Column.Type.binary, 
            'int':Column.Type.int }.iteritems():
            if db_field_type == field_type:
                return column_type
        raise Exception('Can not support %s field type !' % db_field_type)

    def commit(self):
        self._conn.commit()

    def _reconnect(self):
        self.close()
        self._conn = MySQLdb.connect(**self._db_args)
        self._conn.autocommit(True)
    
    def _cursor(self):
        return self._conn.cursor()

    def close(self):
        try:
            if self._conn:
                self._conn.close()
        finally:
            self._conn = None
    
    def __del__(self):
        self.close()

    def __show_sql(self, sql, params):
        if not params:
            return sql
        else:
            formated_params = []
            for param in params:
                if is_str(param):
                    param = "'%s'" % MySQLdb.escape_string(param)
                elif is_date(param):
                    param = "'%s'" % str2date(param)
                elif is_datetime(param):
                    param = "'%s'" % str2datetime(param)
                else:
                    param = str(param)
                formated_params.append(param)
            formated_params.append(';')
            return ''.join(flatten(izip(sql.split('?'), formated_params)))
