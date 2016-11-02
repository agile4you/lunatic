from distutils.core import setup
from lunatic import __version__

version = __version__

setup(
    name='lunatic',
    version=version,
    packages=['lunatic'],
    url='https://github.com/agile4you/lunatic',
    requires=[
        'psycopg2',
        'gevent',
        'psycogreen',
        'psycogreen',
        'ujson',
        'sqlalchemy',
        'snaql'
    ],
    license='GLPv3',
    author='Papavassiliou Vassilis',
    author_email='vpapavasil@gmail.com',
    description='PostgreSQL Python booster utilities'
)
