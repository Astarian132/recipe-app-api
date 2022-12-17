"""
Django command to wait for the database to be avalivable
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    "Django command to wait for database."

    def handle(self, *args, **options):
        "Entrypoint for command"
        self.stdout.write('Waiting for database...')
        db_up = False                                   # asume db is not ready
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True                             # set db as ready
            except (Psycopg2OpError, OperationalError):  # unless it's not
                self.stdout.write('Database unavalivable, waiting 1 second...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database avalivable!'))
