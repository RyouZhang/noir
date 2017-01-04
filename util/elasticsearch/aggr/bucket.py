from .base import *


__all__ = (
    'Terms',
)


class Terms(ESBucketClause):

    def __init__(self, field, size):
        super(Terms, self).__init__()
        self['terms'] = dict(field=field, size=size)