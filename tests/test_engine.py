# -*- coding: utf-8 -*-
"""'lunatic.engine' module unittest suite.
"""

import pytest
from lunatic.engine import DBEngineError, DBRouterError


def test_db_router_container_protocol(db_router, db_engine):
    """Unit Tests for `lunatic.engine.DBRouter` container protocol.
    """
    assert db_router['master']

    with pytest.raises(DBRouterError):
        db_router['slave'] = 'Bad_database'

    db_router['slave'] = db_engine

    assert 'slave' in db_router

    del db_router['slave']

    assert db_router.engines == ('master', )


def test_db_router_proxy_method_single_record(db_router):
    """Unit test for `lunatic.engine.DBRouter.proxy` method for single record.
    """

    record = db_router.proxy('Select 2 as number;', fetch_many=False)

    assert record == {'number': 2}


def test_db_router_proxy_method_multiple_record(db_router):
    """Unit test for `lunatic.engine.DBRouter.proxy` method for multiple records.
    """
    record = db_router.proxy('Select x from generate_series(1, 3) x;')

    assert record == [{'x': 1}, {'x': 2}, {'x': 3}]


def test_db_router_proxy_method_backend_error(db_router):
    """Unit test for `lunatic.engine.DBRouter.proxy` method for error handling.
    """
    with pytest.raises(DBEngineError):
        assert db_router.proxy('Select what_ever;')

