#-*- coding: utf-8 -*-


"""OAuth 2.0 Response Types"""


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
    combs = combinations(RESPONSE_OPTIONS, x)
    RESPONSE_CHOICES += [reduce(lambda a, b:a|b, y) for y in combs]


class InvalidResponseType(OAuth2Exception):
    """Raised when is_valid_response_type encounters an invalid 
    response type."""
    pass


def is_valid_response_type(x, y):
    """Checks if response type x is a subset of response set range y."""
    if x not in RESPONSE_CHOICES:
        raise InvalidResponseType("Invalid response type: %s" % x)
    if y not in RESPONSE_CHOICES:
        raise InvalidResponseType("Invalid response type: %s" % y)
    return x & y != 0