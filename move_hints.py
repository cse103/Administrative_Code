import pandas as pd
import argparse
import datetime
import getpass

from sqlalchemy import *
from sqlalchemy.sql import *
from sqlalchemy.dialects.mysql import \
        BIGINT, BINARY, BIT, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, DOUBLE, ENUM, FLOAT, INTEGER, \
        LONGBLOB, LONGTEXT, MEDIUMBLOB, MEDIUMINT, MEDIUMTEXT, NCHAR, \
        NUMERIC, NVARCHAR, REAL, SET, SMALLINT, TEXT, TIME, TIMESTAMP, \
        TINYBLOB, TINYINT, TINYTEXT, VARBINARY, VARCHAR, YEAR

from IPython import embed

db = 'webwork'

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Copy hints from old problems to new ones")
    parser.add_argument('--csv', help="Problem table", default="set_assignments.csv")
    parser.add_argument('--course', help="Course", default="CSE103_Fall14")
    parser.add_argument('-u', '--username', help="MySQL username", default="webworkWrite")
    parser.add_argument('-p', '--password', help="MySQL password", action='store_true')
    args = parser.parse_args()
    if args.password:
        mysql_password = getpass.getpass()
    engine = create_engine('mysql+mysqldb://{0}:{1}@localhost/{2}'.format(args.username, mysql_password, db), pool_recycle=3600)
    metadata = MetaData()
    conn = engine.connect()

    hints_table = Table("{0}_hint".format(args.course), metadata,
                      Column('id', Integer, nullable=False, primary_key=True),
                      Column('pg_text', String(65536), nullable=False),
                      Column('author', String(255), nullable=False),
                      Column('set_id', String(255), nullable=False),
                      Column('problem_id', Integer, nullable=False),
                      Column('part_id', Integer),
                      Column('created', TIMESTAMP),
                      Column('deleted', Boolean)
    )

    problems_table = Table("{0}_problem".format(args.course), metadata,
                           Column('set_id', TINYBLOB, nullable=False),
                           Column('problem_id', Integer, nullable=False),
                           Column('source_file', Text),
                           Column('value', Integer),
                           Column('max_attempts', Integer),
                           Column('flags', Text)
    )

    df = pd.read_csv('set_assignments.csv')
    for index, problem in df.iterrows():
        print problem
        new_problem = conn.execute(
            select([problems_table]).where(problems_table.c.source_file == problem['PG File Path'])).fetchone()
        print new_problem
        old_path = problem['Original Path']
        old_problems = conn.execute(select([problems_table.c.set_id, problems_table.c.problem_id, problems_table.c.source_file]).where(problems_table.c.source_file==old_path))
        for old_problem in old_problems:
            print old_problem
            old_hints = conn.execute(select([hints_table]).where(hints_table.c.set_id==old_problem.set_id).where(hints_table.c.problem_id == old_problem.problem_id))
            for hint in old_hints:
                row_val = dict(hint.items())
                row_val.pop('id')
                print row_val
                row_val['set_id'] = new_problem.set_id
                row_val['problem_id'] = new_problem.problem_id
                ins = hints_table.insert().values(**row_val)
                res = conn.execute(ins)
        print 
