# -*- coding: utf-8 -*-
"""`lunatic.errors` module.

Provides package base error classes.
"""


class LunaticError(Exception):
    """Base package Error class.
    """
    pass


class QueryManagerError(LunaticError):
    """QueryManager Error class.
    """
    pass


class DBEngineError(LunaticError):
    """DBEngine base Error.
    """
    pass


class DBRouterError(DBEngineError):
    """DBRouter Error.
    """
    pass
