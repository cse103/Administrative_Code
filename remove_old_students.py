#!/usr/bin/env python

import argparse
from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR
import pandas as pd

def get_students(user_tbl, permissions_tbl, connection):
    s = select([user_tbl, permissions_tbl.c.permission]).\
        select_from(user_tbl.join(permissions_tbl, user_tbl.c.user_id==permissions_tbl.c.user_id)).\
        where(permissions_tbl.c.permission == 0)
    return connection.execute(s)

def select_students(user_tbl, permissions_tbl):
    s = select([user_tbl, permissions_tbl.c.permission]).\
        select_from(user_tbl.join(permissions_tbl, user_tbl.c.user_id==permissions_tbl.c.user_id)).\
        where(permissions_tbl.c.permission == 0)
    return s

def get_staff(user_tbl, permissions_tbl, connection):
    s = select([user_tbl, permissions_tbl.c.permission]).\
        select_from(user_tbl.join(permissions_tbl, user_tbl.c.user_id==permissions_tbl.c.user_id)).\
        where(permissions_tbl.c.permission != 0)
    return connection.execute(s)

def delete_students(course, students):
    pass

def connect_db(username, password, database):
    engine = create_engine('mysql+mysqldb://{0}:{1}@localhost/{2}'.
                           format(username, password, database), pool_recycle=3600)
    metadata = MetaData()
    return engine, metadata

def users_table(course, metadata):
    """
    user_id       | tinyblob
    first_name    | text
    last_name     | text
    email_address | text
    student_id    | text
    status        | text
    section       | text
    recitation    | text
    comment       | text
    """
    tbl = Table("{0}_user".format(course), metadata,
                Column('user_id', TINYBLOB, nullable=False, primary_key=True),
                Column('first_name', Text),
                Column('last_name', Text),
                Column('email_address', Text),
                Column('student_id', Text),
                Column('status', Text),
                Column('section', Text),
                Column('recitation', Text),
                Column('comment', Text)
    )
    return tbl

def permissions_table(course, metadata):
    tbl = Table("{0}_permission".format(course), metadata,
                Column('user_id', TINYBLOB, nullable=False),
                Column('permission', Integer)
    )
    return tbl;


def remove_old_students(old_course, new_course, username, password, csv):
    engine, metadata = connect_db(username, password, 'webwork')
    old_users_table = users_table(old_course, metadata)
    old_perms_table = permissions_table(old_course, metadata)
    new_users_table = users_table(new_course, metadata)
    new_perms_table = permissions_table(new_course, metadata)
    connection = engine.connect()
    old_students = get_students(old_users_table, old_perms_table, engine)

    if csv:
        roster = pd.read_csv(csv)
        current_student_emails = set(roster['Email'])
    students_to_remove = []
    for row in old_students:
        if csv and row.email_address in current_student_emails:
            print "Not removing {0} because they're in the current roster".format(row.user_id)
        else:
            students_to_remove.append(row.user_id)
    print "Removing ", students_to_remove

    s_remove = select_students(new_users_table, new_perms_table).where(new_users_table.c.user_id.in_(students_to_remove))

    print connection.execute(s_remove).fetchall()
    s_del = new_users_table.delete().where(new_users_table.c.user_id.in_(students_to_remove))

    result = connection.execute(s_del)
    print result.rowcount, "students deleted"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('old', help="Old Course", default="UCSD_CSE103")
    parser.add_argument('new', help="New Course", default="CSE103_Fall14")
    parser.add_argument('--user', help="MySQL username", default="webworkWrite")
    parser.add_argument('--password', help='MySQL password', default="webwork")
    parser.add_argument('--csv', help="Student roster in CSV form")
    args = parser.parse_args()
    remove_old_students(args.old, args.new, args.user, args.password, args.csv)
