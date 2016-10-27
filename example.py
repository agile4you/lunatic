from lunatic import pubsub
import ujson


cache_chanel = pubsub.connect(
    database='entityDB',
    port=5432,
    host='localhost',
    user='pav',
    password='iverson'
)


cache_chanel.listen('cache')

for event in cache_chanel.events():
    print(ujson.loads(event.payload))
