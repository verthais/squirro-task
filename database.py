import sqlite3
import logging
from schema import Schema
from uuid import uuid4, UUID

class DatabaseError(Exception):
    "Error for the database events"

class Database():
    table_name = None
    schema = None
    def __init__(self,):
        self.database_name = None
        # TODO: make connection share and sustainable
        self.connection = None

    @classmethod
    def create(cls, database_name: str) -> None:
        '''
            args:
                database_name: str - target database name for table creation
        '''
        logger = logging.getLogger(f'DB:create:{cls.table_name}')
        cmd = "CREATE TABLE {table}({columns})"
        cols = ','.join(cls.schema.schema.keys())
        cmd = cmd.format(
            table=cls.table_name,
            columns=cols
        )

        connection = sqlite3.connect(database_name)
        currsor = connection.cursor()

        logger.info('Creating table %s -- %s', cls.table_name, cmd)
        currsor.execute(cmd)
        connection.commit()
        connection.close()

    def _get_cmd(self, cmd, **kwargs):
        if kwargs.get('where'):
            sep = ''
            condition = 'WHERE '
            for key, val in kwargs.get('where').items():
                condition += f'{sep}{key} = "{val}"'
                sep = ' AND '

        if kwargs.get('col'):
            cols = ','.join(kwargs.get('col'))
        else:
            cols = ','.join(self.schema.schema.keys())


        return cmd.format(
            col = cols ,
            table = self.table_name,
            condition = f'{condition}',
        )


    def _put_cmd(self, cmd, id, **kwargs):
        if kwargs.get('values'):
            # TODO: support all types
            values = f'"{str(id)}","' + '","'.join(kwargs.get('values')) + '"'
        else:
            raise DatabaseError('no values to insert')

        return cmd.format(
            table = self.table_name,
            values = values,
        )

    def connect(self, database_name: str):
        self.database_name = database_name
        self.connection = sqlite3.connect(self.database_name)

    def get(self, **kwargs) -> list:
        '''
            kwargs:
                dry_run: bool - flag to get the raw querry
                where: dict   - col_name:value pairs to match in where statement
                col: list     - column names to return values for

            returns:
                list(tuple(col[,col...]))
        '''
        cmd = 'SELECT {col} FROM {table} {condition}'
        cmd = self._get_cmd(cmd, **kwargs)

        if kwargs.get('dry_run'):
            return cmd

        cur = self.connection.cursor()
        data = list(cur.execute(cmd))
        return data

    def put(self, **kwargs) -> UUID:
        '''
            kwargs:
                dry_run: bool - flag to get the raw querry
                values: list - in order list of values to insert

            returns:
                uuid: str    - returns the id of the newly created entity
        '''
        id = uuid4()
        cmd = "INSERT INTO {table} VALUES ({values})"
        cmd = self._put_cmd(cmd, id, **kwargs)

        if kwargs.get('dry_run'):
            return cmd

        cur = self.connection.cursor()
        cur.execute(cmd)
        self.connection.commit()

        return id


class Text(Database):
    table_name = 'texts'
    schema = Schema({
        'id': str,
        'content': str,
    })
    def __init__(self):
        super().__init__()


class Summary(Database):
    table_name = 'summaries'
    schema = Schema({
        'id': str,
        'text_id': str,
        'summary': str,
    })
    def __init__(self):
        super().__init__()


def migrate(database_name) -> None:
    'initialize database'
    tables = [
        Text,
        Summary,
    ]

    for table in tables:
        table.create(database_name)