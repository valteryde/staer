
# *** libs ***
import sqlite3
import re
from datetime import date
import os


# *** helper ***
NOT_ALLOWED = [('"', 'char1'), ("'", 'char2')]
def sanitize(w):
    if type(w) is not str:
        return w
    for na, rep in NOT_ALLOWED:
        w = re.sub(na, rep, w)
    return w


# *** sqlite db ***
class SQLiteDB:

    def __init__(self, name):
        if 'database' not in os.listdir():
            os.mkdir('database')
        self.new = False
        if name not in os.listdir('database'):
            self.new = True
        self.con = sqlite3.connect(os.path.join('database',name))
        self.cursor = self.con.cursor()


    # helper
    def date(self):
        today = date.today()
        return str(today.strftime("%Y/%m/%d"))

    def _sanitize_list_(self, l):
        values = list(map(sanitize, l))

        for i in range(len(values)):
            if values[i] == None:
                values[i] = 'null'

            elif type(values[i]) is str:
                values[i] = '"{}"'.format(values[i])

        return values


    # main
    def get(self, select_, from_, where_=None, sql=None):
        if sql:
            return
        if type(from_) is list:
            from_ = ','.join(from_)
        if type(select_) is list:
            select_ = ','.join(select_)

        sql = 'SELECT {} FROM {}'.format(sanitize(select_), sanitize(from_))
        if where_:
            sql += ' WHERE {}'.format(where_)

        self.cursor.execute(sql)
        return self.cursor.fetchall()


    def insert(self, table, values):
        values = self._sanitize_list_(values)

        values = list(map(str,values))
        self.cursor.execute('INSERT INTO {} VALUES ({})'.format(sanitize(table),','.join(values)))
        self.con.commit()


    def remove(self, table, where_, values): #where_ = 'id = {}'
        if type(values) is not list and type(values) is not tuple: #if values is value
            values = [values]

        try:
            sql = 'DELETE FROM {} WHERE {};'.format(sanitize(table),where_.format(*self._sanitize_list_(values)))
        except IndexError:
            return 'IndexError'

        self.cursor.execute(sql)
        self.con.commit()
        return True


    def update(self, table, set, where):
        sql = 'UPDATE {} SET {} WHERE {}'.format(sanitize(table), set, where)
        self.cursor.execute(sql)
        self.con.commit()
        return True


    def setup(self, config:dict):
        #print(config)

        """
        CREATE TABLE Shop (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        	title TEXT NOT NULL,
        	date_of_creation TEXT,
        	price INTEGER,
        	status INTEGER NOT NULL,
            desc TEXT NOT NULL,
            size TEXT NOT NULL,
        	image_ref INTEGER REFERENCES Image (id)
        );
        """

        #{'name':'id', 'type':'number', 'primary':True, 'reference':(), 'not_null':True, 'autoincrement':True},

        sql = ''
        for table in config:
            sql += 'CREATE TABLE {} (\n'.format(table)

            for section in config[table]:
                line = '{} {}'.format(section['name'], section['type'].upper())

                if section.get('not_null', None):
                    line += ' NOT NULL'
                if section.get('primary', None):
                    line += ' PRIMARY KEY'
                if section.get('autoincrement', None):
                    line += ' AUTOINCREMENT'
                if section.get('reference', None) not in [False, None, 0]:
                    ref = section.get('reference', None)
                    line += ' REFERENCES {} ({})'.format(*ref)
                sql += line + ',\n'
            sql = sql[:-2]+'\n'
            sql += ')\n'

        self.cursor.execute(sql)
        self.con.commit()


    def close(self):
        self.con.close()
