#-*- coding: utf-8 -*-


"""OAuth 2.0 URI Helper Functions"""


from urlparse import urlparse, urlunparse, parse_qsl
from urllib import urlencode
from url_normalize import url_normalize
 
 
def add_parameters(url, parameters):
    """Parses URL and appends parameters. 

    **Args:**

    * *url:* URL string.
    * *parameters:* Dict of parameters

    *Returns str*"""
    parts = list(urlparse(url))
    parts[4] = urlencode(parse_qsl(parts[4]) + parameters.items())
    return urlunparse(parts)
    

def add_fragments(url, fragments):
    """Parses URL and appends fragments. 

    **Args:**

    * *url:* URL string.
    * *fragments:* Dict of fragments

    *Returns str*"""
    parts = list(urlparse(url))
    parts[5] = urlencode(parse_qsl(parts[5]) + fragments.items())
    return urlunparse(parts)
    
    
def normalize(url):
    """Normalizes URL.

    **Args:**

    * *url:* URL string.

    *Returns str*"""
    return url_normalize(url)
    