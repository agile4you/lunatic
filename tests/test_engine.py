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


def test_db_router_proxy_method(db_router):
    """Unit test for `lunatic.engine.DBRouter.proxy` method.
    """

    record = db_router.proxy('Select 2 as number;', fetch_many=False)

    assert record == {'number': 2}

    with pytest.raises(DBEngineError):
        assert db_router('Select what_ever;')
