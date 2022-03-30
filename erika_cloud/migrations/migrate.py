# For relative imports to work in Python 3.6
import sys; sys.path.append("..")

from playhouse.migrate import *
from peewee import BooleanField
import models
from datetime import datetime

db = SqliteDatabase(models.DB_FILE_PATH)
migrator = SqliteMigrator(db)

def add_last_seen():
    last_seen_field = DateTimeField(default=datetime.now)
    migrate(
        migrator.add_column('typewriter', 'last_seen', last_seen_field)
    )

def add_is_printed():
    is_printed_field = BooleanField(default=False)
    migrate(
        migrator.add_column('message', 'is_printed', is_printed_field)
    )



if __name__ == '__main__':

    migrations = [
        "add_last_seen",
        "migrate(migrator.add_index('typewriter', ('uuid', ), unique=True))",
        "migrate(migrator.add_index('typewriter', ('erika_name', ), unique=True))",
        "add_is_printed"
    ]

    for m in migrations:
        try:
            eval(m + '()')
            print("OK: function `" + m + "` successfull.")
        except Exception as e:
            print("ERROR: " + str(e))