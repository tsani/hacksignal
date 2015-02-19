from app import app

import psycopg2

class Database:
    connection = None

    @classmethod
    def get_connection(cls):
        if Database.connection is None:
            Database.connection = psycopg2.connect(
                    "dbname='%s' user='%s' password='%s' host='%s'" %
                    tuple(app.config['DATABASE'][k]
                        for k in ['name', 'user', 'password', 'host']))
        return Database.connection

