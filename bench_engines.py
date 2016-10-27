from gevent import monkey
from lunatic.patch import psycopg_patch

# do the patching
monkey.patch_all()
psycopg_patch()


import bottle
from lunatic.engine import DBRouter


SAMPLE_QS = """select uid, record_data from resource.records where record_data @> '{"type": "admin"}' limit 10;"""


DATABASES = {
    'master': {'conn_uri': 'postgresql://pav:iverson@localhost:6432/resource_db', 'gevent_enabled': True},
    'slave': {'conn_uri': 'postgresql://pav:iverson@localhost:6432/resource_db_slave', 'gevent_enabled': True}
}


db_backend = DBRouter.dict_config(**DATABASES)


@bottle.get('/')
def api():
    records = db_backend.proxy(SAMPLE_QS)
    return {"data": records}

bottle.run(host='0.0.0.0', port=9023, reloader=True, server='gevent', spawn=600)
