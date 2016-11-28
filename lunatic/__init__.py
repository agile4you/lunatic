# -*- coding: utf-8 -*-
#
#    Copyright (C) 2015  Papavassiliou Vassilis
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""`lunatic` package.

Postgresql python booster package!
"""

__all__ = ('DBEngine', 'DBEngineError', 'DBRouter', 'DBRouterError', 'QueryManager', 'QueryManagerError',
           'pubsub', 'patch')

__version__ = '1.1.5'

from lunatic.engine import DBEngine, DBRouter
from lunatic.query import QueryManager
import lunatic.pubsub
import lunatic.patch
from lunatic.errors import (DBRouterError, DBEngineError, LunaticError, QueryManagerError)
import logging


logging.getLogger('lunatic')
