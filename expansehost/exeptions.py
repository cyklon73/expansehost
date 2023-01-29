class UnauthorizedError(IOError):
    """You are unauthorized"""


class InvalidParameterError(IOError):
    """parameter is invalid"""


class MissingParameterError(InvalidParameterError):
    """"missing required parameter"""
