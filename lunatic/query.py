# -*- coding: utf-8 -*-
"""`lunatic.query` module.

Provides a query interface for interacting with `lunatic.engine.DBEngine`
objects.
"""

__all__ = ('QueryManager', )

import logging
from lunatic.errors import DBEngineError, DBRouterError, QueryManagerError
from snaql.factory import Snaql, SnaqlException
from snaql.convertors import SnaqlGuardException
from jinja2.exceptions import TemplateNotFound
from functools import wraps


class QueryManager(object):
    """Base query manager class.
    """

    debug = True
    logger = logging.getLogger(__name__)

    def __init__(self, engine=None):
        self.engine = engine
        self.builder = None

    def load(self, query_parent, query_dir, query_file):
        """Load queries from template files to instance attributes.

        Args:
            query_parent (str): Query folder parent directory
            query_dir (str): Query folder name
            query_file (str): Query file name.

        Returns:
            The QueryManager instance.

        Raises:
            QueryManagerError, if any snaql Exception occurs.
        """
        try:
            self.builder = Snaql(query_parent, query_dir).load_queries(query_file)
        except (SnaqlException, TemplateNotFound) as error:
            raise QueryManagerError(error.args)

        self.mount()

        return self

    @property
    def proxy_rule(self):
        return [method for method in dir(self.builder)
                if not method.startswith('_')
                and hasattr(getattr(self.builder, method), 'func_name')]

    def mount(self):
        """Mount snaql queries instance.
        """

        def proxy_wrapper(func):
            @wraps(func)
            def _wrapper(*args, **kwargs):
                """Inner wrapper for proxy methods.
                """
                fetch_many = kwargs.pop('fetch_many', True)

                try:
                    queryset = func(*args, **kwargs)
                    if self.debug:
                        self.logger.info('Execute: {}'.format(queryset))
                    records = self.engine.query(queryset, fetch_many)

                except (SnaqlException, SnaqlGuardException, DBRouterError, DBEngineError) as error:
                    self.logger.error(error.args[0])
                    raise QueryManagerError(error.args[0])

                return records

            return _wrapper

        for proxy in self.proxy_rule:
            setattr(self, proxy, proxy_wrapper(getattr(self.builder, proxy)))

        return self

