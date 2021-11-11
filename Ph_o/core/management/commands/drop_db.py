import psycopg2
import os
import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **options):
        #establishing the connection
        conn = psycopg2.connect(
            database=os.environ.get('DB_NAME'), user=os.environ.get('DB_USER'), password=os.environ.get('DB_PASS'),
            host='127.0.0.1', port= '5432'
        )

        #Setting auto commit false
        conn.autocommit = True

        #Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        #Doping EMPLOYEE table if already exists
        cursor.execute("DROP TABLE emp")
        print("Table dropped... ")

        #Commit your changes in the database
        conn.commit()

        #Closing the connection
        conn.close()
