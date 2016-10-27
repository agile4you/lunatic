# -*- coding: utf-8 -*-
"""
"""

__all__ = ('psycopg_patch',)

from psycogreen.gevent import patch_psycopg
import json
import psycopg2.extras


def psycopg_patch():
    """Gevent patching.
    """

    patch_psycopg()

    def jsonb_loads(stream):
        return json.loads(stream, object_pairs_hook=OrderedDict)

    psycopg2.extras.register_default_json(globally=True, loads=jsonb_loads)



