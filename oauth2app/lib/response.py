#-*- coding: utf-8 -*-


from ..exceptions import OAuth2Exception
from itertools import combinations

TOKEN = 1
CODE = 2
CODE_AND_TOKEN = 4
RESPONSE_TYPES = {
    "token":TOKEN,
    "code":CODE,
    "code_and_token":CODE_AND_TOKEN}
RESPONSE_OPTIONS = RESPONSE_TYPES.values()
RESPONSE_CHOICES = []
for x in range(1, len(RESPONSE_OPTIONS) + 1):
    RESPONSE_CHOICES += [reduce(lambda a, b:a|b, y) for y in combinations(RESPONSE_OPTIONS, x)]


class InvalidResponseType(OAuth2Exception):
    pass


def reduce_response_types(*args):
    for x in args:
        if x not in RESPONSE_OPTIONS:
            raise InvalidResponseType("Invalid response type: %s" % x)
    return reduce(lambda x, y: x|y, args)


def is_valid_response_type(x, y):
    if x not in RESPONSE_CHOICES:
        raise InvalidResponseType("Invalid response type: %s" % x)
    if y not in RESPONSE_CHOICES:
        raise InvalidResponseType("Invalid response type: %s" % y)
    return x & y != 0