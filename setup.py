from distutils.core import setup
from lunatic import __version__

version = '.'.join(__version__)

setup(
    name='lunatic',
    version=version,
    packages=['lunatic'],
    url='https://github.com/agile4you/lunatic',
    install_requires=[
        'psycopg2',
        'gevent',
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
