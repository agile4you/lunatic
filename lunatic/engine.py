# -*- coding: utf-8 -*-
""" `lunatic.pool` module.

Provides a high level connection pooling for Postgresql servers.
"""


__all__ = ('DBEngine', 'DBRouter', 'DBEngineError', 'DBRouterError')


import logging
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool, QueuePool
from itertools import cycle
from sqlalchemy.exc import ProgrammingError, OperationalError, DatabaseError, DataError
from lunatic.errors import DBEngineError, DBRouterError


class DBEngine(object):
    """Postgresql database connection engine class.

    Provides a wrapper on sqlalchemy DBAPI-2 implementation implementing
    a concrete and simple API.

    Attributes:
        conn_uri (str): PostgreSQL connection info.
        pool_type (object): SQLAlchemy pool factory class.
        engine (object): SQLAlchemy Engine instance.
        debug (bool): Set DEBUG mode on / off.


    Raises:
        DBEngineError, if any exception occurs.
    """

    __slots__ = ('conn_uri', 'pool_type', '_engine', 'debug')

    logger = logging.getLogger(__name__)

    pool_factory = (
        ('null', NullPool),
        ('queue', QueuePool)
    )

    def __init__(self, conn_uri='', pool_factory='null', debug=True, **conn_data):
        self.conn_uri = conn_uri if conn_uri else self.pg_uri(**conn_data)
        self.pool_type = dict(self.pool_factory).get(pool_factory, NullPool)
        self.debug = debug
        self._engine = None

    @property
    def engine(self):
        """Lazy initialize DBAPI-2 connection protocol.
        """
        if not self._engine:
            self._engine = create_engine(
                self.conn_uri,
                poolclass=self.pool_type,
                isolation_level='AUTOCOMMIT'
            )

            self._engine._use_thread_local = True

            if self.debug:  # pragma: no cover
                self.logger.info('Initialized pool: {}'.format(self.conn_uri))

        return self._engine

    def query(self, qs, fetch_many=True):
        """Execute query within engine.

        Args:
            qs (str): Plain text query.
            fetch_many (boolean)
        Returns:
            Query Records or None.

        Raises:
            DBEngineError, if a connection / data Error occurs.
        """
        try:
            record_proxy = self.engine.execute(qs)

        except (ProgrammingError, OperationalError, DatabaseError, DataError) as error:
            self.logger.debug('Error Encountered: {}'.format(error.args[0]))
            raise DBEngineError(error.args[0])

        records = [{key: row[key] for key in record_proxy.keys()} for row in record_proxy]

        if self.debug:  # pragma: no cover
            self.logger.info('SQL: {}'.format(qs))

        if fetch_many:
            return records or []

        return records[0] if records else None

    @staticmethod
    def pg_uri(host='localhost', port=5432, database='postgres', user='postgres', password=None):
        """Return a PostgreSQL connection URI for the specified values.

        Args:
            host (str): Host to connect to
            port (int): Port to connect on
            database (str): The database name
            user (str): User to connect as
            password (str): The password to use, None for no password

        Returns:
            A valid PostgreSQL connection URI.
        """
        if port:
            host = '{}:{}'.format(host, port)

        if password:
            return 'postgresql://{}:{}@{}/{}'.format(user, password, host, database)

        return 'postgresql://{}@{}/{}'.format(user, host, database)

    def __repr__(self):  # pragma: no cover
        return '<DBEngine instance at: 0x{:x}>'.format(id(self))

    def __str__(self):  # pragma: no cover
        return '<DBEngine({})>'.format(self.conn_uri)

    def __call__(self, qs, fetch_many=True):  # pragma: no cover
        return self.query(qs, fetch_many)


class DBRouter(object):
    """DBEngine Router class.

    Manages multiple DBEngine instances. `DBRouter` instances
    implements round robin load balance protocol.

    Attributes:
        _engines (dict): a mapping of aliases / DBEngine instances for management.
    """

    logger = logging.getLogger(__name__)

    __slots__ = ('_engines', 'router', 'debug')

    def __init__(self, debug=True, **engines):
        self._engines = engines or {}
        self.debug = debug
        self.router = cycle(engines.keys())

    @classmethod
    def dict_config(cls, **config):
        """Initialize DBRouter from a dictionary/

        Args:
            config (): A mapping of aliases / DBEngine initialization parameters.

        Returns:
            DBRouter instance.
        """
        return cls(**{key: DBEngine(**config[key]) for key in config})

    @property
    def engines(self):
        return tuple(self._engines.keys())

    def query(self, qs, fetch_many=True):
        """Execute query within an managed engine.

        Args:
            qs (str): Plain text query.
            fetch_many (boolean)
        Returns:
            Query Records or None.

        Raises:
            DBEngineError, if a connection / data Error occurs.
        """

        db_route = next(self.router)

        if self.debug:  # pragma: no cover
            self.logger.info('Routing query to: {}'.format(db_route))
            return self._engines.get(db_route).query(qs, fetch_many)

    def __call__(self, qs, fetch_many=True):
        return self.proxy_query(qs, fetch_many)

    def __getitem__(self, item):
        return self._engines[item]

    def __contains__(self, item):
        return item in self.engines

    def __setitem__(self, key, value):
        if not isinstance(value, DBEngine):
            raise DBRouterError('DBRouter accepts only `lunatic.DBEngine` instances.')
        self._engines[key] = value
        self.router = cycle(self.engines)

    def __delitem__(self, key):
        del self._engines[key]
        self.router = cycle(self.engines)
