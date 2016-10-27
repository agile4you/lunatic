# -*- coding: utf-8 -*-
"""'lunatic' package fixtures module.
"""

import pytest
from lunatic.engine import DBRouter, DBEngine


@pytest.fixture(scope='session')
def db_router():
    """pytest fixture for `lunatic.DBRouter` class instance.
    """
    db_setup = {'master': {'user': 'postgres', 'database': 'travis_ci_test'}}

    db_router = DBRouter.dict_config(**db_setup)

    return db_router


@pytest.fixture(scope='session')
def db_engine():
    """pytest fixture for `lunatic.DBEngine` class instance.
    """
    db_engine = DBEngine(user='postgres', database='travis_ci_test_1')

    return db_engine
