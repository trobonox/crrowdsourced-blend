import sqlite3, logging
from os.path import isfile

db_path = "./db/picks.db"
tables_path = "./db/tables.sql"

connection = sqlite3.connect(db_path, check_same_thread=False)
cursor = connection.cursor()

# create commit decorator
def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        connection.commit()

    return inner

@with_commit
def build_initial_tables():
    if isfile(tables_path):
        execute_script(tables_path)


# methods for selection
def get_records(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchall()


def get_record(command, *values):
    cursor.execute(command, tuple(values))
    return cursor.fetchone()


def get_column(command, *values):
    cursor.execute(command, tuple(values))

    return [item[0] for item in cursor.fetchall()]


def field(command, *values):
    cursor.execute(command, tuple(values))
    fetch = cursor.fetchone()
    if fetch is not None:
        return fetch[0]


# execute
def execute(command, *values):
    cursor.execute(command, tuple(values))


def multiexec(command, valueset):
    cursor.executemany(command, valueset)


def execute_script(path):
    with open(path, "r", encoding="utf-8") as script:
        cursor.executescript(script.read())


# essential - close & init
def init_db():
    build_initial_tables()
    logging.info("Initialized database.")
    return (connection, cursor)


def get_db_connection():
    return (connection, cursor)


def close_connection():
    connection.close()