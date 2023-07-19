"""
Exceptions
==========

Specific application exceptions.
"""


class MakevokeBaseException(Exception):
    """
    Exception base.

    You should never use it directly except for test purpose. Instead make or
    use a dedicated exception related to the error context.
    """
    pass


class MakevokeContextError(MakevokeBaseException):
    """
    An exception related to set/get context
    """
    pass
