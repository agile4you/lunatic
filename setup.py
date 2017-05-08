from distutils.core import setup
import re
import ast


_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('lunatic/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')
    ).group(1)))


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
