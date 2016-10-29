# -*- coding: utf-8 -*-
"""
"""

__all__ = ('psycopg_to_gevent', 'json_to_ordered_dict')

from collections import OrderedDict
from psycogreen.gevent import patch_psycopg
import json
import psycopg2.extras


def psycopg_to_gevent():
    """`psycogreen.gevent` shortcut.
    """
    patch_psycopg()


def json_to_ordered_dict():
    """Return PostgreSQL JSON/JSONB types to python OrderedDict.
    """
    def jsonb_loads(stream):
        return json.loads(stream, object_pairs_hook=OrderedDict)

    psycopg2.extras.register_default_json(globally=True, loads=jsonb_loads)
