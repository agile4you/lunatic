from distutils.core import setup
from lunatic import  __version__

version = '.'.join(__version__)

setup(
    name='lunatic',
    version=version,
    packages=['tests', 'lunatic'],
    url='https://github.com/agile4you/lunatic',
    license='GLPv3',
    author='pav',
    author_email='vpapavasil@gmail.com',
    description='PostgreSQL Python booster utilities'
)
