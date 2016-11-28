# -*- coding: utf-8 -*-
"""'lunatic' package fixtures module.
"""

import pytest
from lunatic.engine import DBRouter, DBEngine
from lunatic.query import QueryManager


@pytest.fixture(scope='session')
def db_router():
    """pytest fixture for `lunatic.engine.DBRouter` class instance.
    """
    db_setup = {'master': {'user': 'postgres', 'database': 'travis_ci_test'}}

    db_router = DBRouter.dict_config(**db_setup)

    return db_router


@pytest.fixture(scope='session')
def db_engine():
    """pytest fixture for `lunatic.engine.DBEngine` class instance.
    """
    db_engine = DBEngine(user='postgres', database='travis_ci_test_1')

    return db_engine


@pytest.fixture(scope='session')
def query_manager(db_engine):
    """pytest fixture for `lunatic.query.QueryManager` class.
    """
    return QueryManager(db_engine)
