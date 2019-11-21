from psycopg2 import pool
import os
from urllib.parse import urlparse


class Database:
    __connection_pool = None

    @classmethod
    def initialise(cls):
        url = urlparse(os.environ.get('DATABASE_URL'))
        #Database.__connection_pool = pool.ThreadedConnectionPool(1, 100, user=url.username, password=url.password,
                                                                 #database=url.path[1:], host=url.hostname)
        Database.__connection_pool = pool.ThreadedConnectionPool(1, 100, user='postgres', password='',
         database='itucsse19', host='localhost')

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection):
        Database.__connection_pool.putconn(connection)

    @classmethod
    def close_all_connections(cls, connection):
        Database.__connection_pool.closeall()


class ConnectionPool:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = Database.get_connection()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            self.connection.rollback()
        else:
            self.cursor.close()
            self.connection.commit()
        Database.return_connection(self.connection)