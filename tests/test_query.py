# -*- coding: utf-8 -*-
"""'lunatic.query' module unittest suite.
"""

import pytest
import os
from lunatic.errors import QueryManagerError


def test_query_manager_load_fail(query_manager):
    """Test query_manager `load` method.
    """

    query_parent = os.path.dirname(os.path.abspath(__file__))
    query_dir = 'test_sql'
    query_file = 'fake.sql'

    with pytest.raises(QueryManagerError):
        query_manager.load(query_parent=query_parent, query_dir=query_dir, query_file=query_file)


def test_query_manager_load_pass(query_manager):
    """Test query_manager `load` method.
    """

    query_parent = os.path.dirname(os.path.abspath(__file__))
    query_dir = 'test_sql'
    query_file = 'test.sql'

    query_manager.load(query_parent=query_parent, query_dir=query_dir, query_file=query_file)

    assert hasattr(query_manager, 'test_query')


def test_query_manager_query_pass(query_manager):
    """Test query manager query execution success.
    """
    query_result = query_manager.test_query(name='Foo', age=34, activate=False, fetch_many=False)

    assert query_result == {'age': 34, 'activated': 0, 'name': 'Foo'}


def test_query_manager_query_fail(query_manager):
    """Test query manager query execution success.
    """
    with pytest.raises(QueryManagerError):
        query_manager.test_query(name='Foo', age='bar', activate=False, fetch_many=False)
