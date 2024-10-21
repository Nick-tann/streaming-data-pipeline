import psycopg2
from functools import cached_property
from dataclasses import dataclass

import psycopg2.extras


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
    dict [key: str, value: any]

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
    
    def insert_table(self,
                     conn : psycopg2.extensions.connection,
                     schema_name: str,
                     table_name: str,
                     table_columns: tuple[str],
                     table_values: list[tuple[any]]
        )->None:
        '''
        Function to insert values into a pgsql table.

        Parameters
        ----------
        cursor: psycopg2.extensions.cursor
        schema_name: str
        table_name: str
        table_columns: tuple[str]
        table_values: list[tuple[any]]

        Returns
        -------
        None
        
        '''

        sql_statement = f"INSERT INTO {self.database}.{schema_name}.{table_name} {table_columns} VALUES %s;"
        psycopg2.extras.execute_values(
            cur = conn.cursor(),
            sql = sql_statement,
            argslist = table_values,
            page_size = 1000
        )
        conn.commit()
        return

    def truncate_table(self,
                     conn : psycopg2.extensions.connection,
                     schema_name: str,
                     table_name: str
        )->None:
        '''
        Function to truncate a pgsql table.

        Parameters
        ----------
        cursor: psycopg2.extensions.cursor
        schema_name: str
        table_name: str

        Returns
        -------
        None
        
        '''
        sql_statement = f"TRUNCATE {self.database}.{schema_name}.{table_name};"
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        conn.commit()
        cursor.close()
        return