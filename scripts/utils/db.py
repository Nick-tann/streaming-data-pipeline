import psycopg2
from functools import cached_property
from dataclasses import dataclass


def create_connection(
    database: str,
    user: str,
    password: str,
    host: str,
    port: str
)-> psycopg2.extensions.connection:
    '''
    Function to create a connection to psycopg2

    Returns
    -------
    psycopg2 Connection object

    '''
    conn = psycopg2.connect(
        database = database,
        user = user,
        password = password,
        host = host,
        port = port
    )
    return conn


@dataclass
class PostgreManager:
    database: str
    user: str
    password: str
    host: str
    port: str

    @property
    def conn(self):
        return create_connection(
            database = self.database,
            user = self.user,
            password = self.password,
            host = self.host,
            port = self.port
        )
    
    @property
    def cursor(self):
        return self.conn.cursor()