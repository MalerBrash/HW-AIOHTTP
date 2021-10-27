
class Base(Exception):
    def __init__(self, message, *args, **kwargs):
        self.message = message


class NotFound(Base):
    reason = 'NotFound'


class ValidateError(Base):
    reason = 'ValidationError'


class HTTPNoContent(Base):
    reason = 'HTTPNoContent'
