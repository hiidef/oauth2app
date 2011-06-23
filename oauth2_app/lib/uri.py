#-*- coding: utf-8 -*-


from urlparse import urlparse, urlunparse, parse_qsl
from urllib import urlencode
from url_normalize import url_normalize
 
 
def add_parameters(url, parameters):
    parts = list(urlparse(url))
    parts[4] = urlencode(parse_qsl(parts[4]) + parameters.items())
    return urlunparse(parts)
    

def add_fragments(url, fragments):
    parts = list(urlparse(url))
    parts[5] = urlencode(parse_qsl(parts[5]) + fragments.items())
    return urlunparse(parts)
    
    
def normalize(url):
    return url_normalize(url)
    