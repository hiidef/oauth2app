#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
URI Normalization function:
 * Take care of IDN domains.
 * Always provide the URI scheme in lowercase characters.
 * Always provide the host, if any, in lowercase characters.
 * Only perform percent-encoding where it is essential.
 * Always use uppercase A-through-F characters when percent-encoding.
 * Prevent dot-segments appearing in non-relative URI paths.
 * For schemes that define a default authority, use an empty authority if the
   default is desired.
 * For schemes that define an empty path to be equivalent to a path of "/",
   use "/".
 * For schemes that define a port, use an empty port if the default is desired
 * All portions of the URI must be utf-8 encoded NFC from Unicode strings

Inspired by Sam Ruby's urlnorm.py: http://intertwingly.net/blog/2004/08/04/Urlnorm
This fork author: Nikolay Panov (<pythoneer@niksite.ru>)

History:
 * 10 Feb 2010: support for shebang (#!) urls
 * 28 Feb 2010: using 'http' schema by default when appropriate
 * 28 Feb 2010: added handling of IDN domains
 * 28 Feb 2010: code pep8-zation
 * 27 Feb 2010: forked from Sam Ruby's urlnorm.py
"""

__license__ = "Python"
__version__ = 1.1

import re
import unicodedata
import urlparse
from urllib import quote, unquote


def url_normalize(url, charset='utf-8'):
    """Sometimes you get an URL by a user that just isn't a real
    URL because it contains unsafe characters like ' ' and so on.  This
    function can fix some of the problems in a similar way browsers
    handle data entered by the user:

    >>> url_fix(u'http://de.wikipedia.org/wiki/Elf (Begriffsklärung)')
    'http://de.wikipedia.org/wiki/Elf%20%28Begriffskl%C3%A4rung%29'

    :param charset: The target charset for the URL if the url was
                    given as unicode string.
    """

    def _clean(string):
        string = unicode(unquote(string), 'utf-8', 'replace')
        return unicodedata.normalize('NFC', string).encode('utf-8')

    default_port = {
        'ftp': 21,
        'telnet': 23,
        'http': 80,
        'gopher': 70,
        'news': 119,
        'nntp': 119,
        'prospero': 191,
        'https': 443,
        'snews': 563,
        'snntp': 563,
    }
    if isinstance(url, unicode):
        url = url.encode(charset, 'ignore')

    # if there is no scheme use http as default scheme
    if url[0] not in ['/', '-'] and ':' not in url[:7]:
        url = 'http://' + url

    # shebang urls support
    url = url.replace('#!', '?_escaped_fragment_=')

    # splitting url to useful parts
    scheme, auth, path, query, fragment = urlparse.urlsplit(url.strip())
    (userinfo, host, port) = re.search('([^@]*@)?([^:]*):?(.*)', auth).groups()

    # Always provide the URI scheme in lowercase characters.
    scheme = scheme.lower()

    # Always provide the host, if any, in lowercase characters.
    host = host.lower()
    if host and host[-1] == '.':
        host = host[:-1]
    # take care about IDN domains
    host = host.decode(charset).encode('idna')  # IDN -> ACE

    # Only perform percent-encoding where it is essential.
    # Always use uppercase A-through-F characters when percent-encoding.
    # All portions of the URI must be utf-8 encoded NFC from Unicode strings
    path = quote(_clean(path), "~:/?#[]@!$&'()*+,;=")
    fragment = quote(_clean(fragment), "~")

    # note care must be taken to only encode & and = characters as values
    query = "&".join(["=".join([quote(_clean(t), "~:/?#[]@!$'()*+,;=") for t in q.split("=", 1)]) for q in query.split("&")])

    # Prevent dot-segments appearing in non-relative URI paths.
    if scheme in ["", "http", "https", "ftp", "file"]:
        output = []
        for part in path.split('/'):
            if part == "":
                if not output:
                    output.append(part)
            elif part == ".":
                pass
            elif part == "..":
                if len(output) > 1:
                    output.pop()
            else:
                output.append(part)
        if part in ["", ".", ".."]:
            output.append("")
        path = '/'.join(output)

    # For schemes that define a default authority, use an empty authority if
    # the default is desired.
    if userinfo in ["@", ":@"]:
        userinfo = ""

    # For schemes that define an empty path to be equivalent to a path of "/",
    # use "/".
    if path == "" and scheme in ["http", "https", "ftp", "file"]:
        path = "/"

    # For schemes that define a port, use an empty port if the default is
    # desired
    if port and scheme in default_port.keys():
        if port.isdigit():
            port = str(int(port))
            if int(port) == default_port[scheme]:
                port = ''

    # Put it all back together again
    auth = (userinfo or "") + host
    if port:
        auth += ":" + port
    if url.endswith("#") and query == "" and fragment == "":
        path += "#"
    return urlparse.urlunsplit((scheme, auth, path, query, fragment))

if __name__ == "__main__":
    import unittest
    suite = unittest.TestSuite()

    """ from http://www.intertwingly.net/wiki/pie/PaceCanonicalIds """
    tests1 = [
        (False, "http://:@example.com/"),
        (False, "http://@example.com/"),
        (False, "http://example.com"),
        (False, "HTTP://example.com/"),
        (False, "http://EXAMPLE.COM/"),
        (False, "http://example.com/%7Ejane"),
        (False, "http://example.com/?q=%C7"),
        (False, "http://example.com/?q=%5c"),
        (False, "http://example.com/?q=C%CC%A7"),
        (False, "http://example.com/a/../a/b"),
        (False, "http://example.com/a/./b"),
        (False, "http://example.com:80/"),
        (True, "http://example.com/"),
        (True, "http://example.com/?q=%C3%87"),
        (True, "http://example.com/?q=%E2%85%A0"),
        (True, "http://example.com/?q=%5C"),
        (True, "http://example.com/~jane"),
        (True, "http://example.com/a/b"),
        (True, "http://example.com:8080/"),
        (True, "http://user:password@example.com/"),

        # from rfc2396bis
        (True, "ftp://ftp.is.co.za/rfc/rfc1808.txt"),
        (True, "http://www.ietf.org/rfc/rfc2396.txt"),
        (True, "ldap://[2001:db8::7]/c=GB?objectClass?one"),
        (True, "mailto:John.Doe@example.com"),
        (True, "news:comp.infosystems.www.servers.unix"),
        (True, "tel:+1-816-555-1212"),
        (True, "telnet://192.0.2.16:80/"),
        (True, "urn:oasis:names:specification:docbook:dtd:xml:4.1.2"),

        # other
        (True, "http://127.0.0.1/"),
        (False, "http://127.0.0.1:80/"),
        (True, "http://www.w3.org/2000/01/rdf-schema#"),
        (False, "http://example.com:081/"),
    ]

    def testcase1(expected, value):

        class test(unittest.TestCase):

            def runTest(self):
                assert (url_normalize(value) == value) == expected, (expected, value, url_normalize(value))
        return test()

    for (expected, value) in tests1:
        suite.addTest(testcase1(expected, value))

    """ mnot test suite; three tests updated for rfc2396bis. """
    tests2 = {
        '/foo/bar/.':
            '/foo/bar/',
        '/foo/bar/./':
            '/foo/bar/',
        '/foo/bar/..':
            '/foo/',
        '/foo/bar/../':
            '/foo/',
        '/foo/bar/../baz':
            '/foo/baz',
        '/foo/bar/../..':
            '/',
        '/foo/bar/../../':
            '/',
        '/foo/bar/../../baz':
            '/baz',
        '/foo/bar/../../../baz':
            '/baz', #was: '/../baz',
        '/foo/bar/../../../../baz':
            '/baz',
        '/./foo':
            '/foo',
        '/../foo':
            '/foo', #was: '/../foo',
        '/foo.':
            '/foo.',
        '/.foo':
            '/.foo',
        '/foo..':
            '/foo..',
        '/..foo':
            '/..foo',
        '/./../foo':
            '/foo', #was: '/../foo',
        '/./foo/.':
            '/foo/',
        '/foo/./bar':
            '/foo/bar',
        '/foo/../bar':
            '/bar',
        '/foo//':
            '/foo/',
        '/foo///bar//':
            '/foo/bar/',
        'http://www.foo.com:80/foo':
            'http://www.foo.com/foo',
        'http://www.foo.com:8000/foo':
            'http://www.foo.com:8000/foo',
        'http://www.foo.com./foo/bar.html':
            'http://www.foo.com/foo/bar.html',
        'http://www.foo.com.:81/foo':
            'http://www.foo.com:81/foo',
        'http://www.foo.com/%7ebar':
            'http://www.foo.com/~bar',
        'http://www.foo.com/%7Ebar':
            'http://www.foo.com/~bar',
        'ftp://user:pass@ftp.foo.net/foo/bar':
             'ftp://user:pass@ftp.foo.net/foo/bar',
        'http://USER:pass@www.Example.COM/foo/bar':
             'http://USER:pass@www.example.com/foo/bar',
        'http://www.example.com./':
            'http://www.example.com/',
        '-':
            '-',
        'пример.испытание/Служебная:Search/Test':
            'http://xn--e1afmkfd.xn--80akhbyknj4f/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:Search/Test',
        'http://lifehacker.com/#!5753509/hello-world-this-is-the-new-lifehacker':
            'http://lifehacker.com/?_escaped_fragment_=5753509/hello-world-this-is-the-new-lifehacker',
    }

    def testcase2(original, normalized):

        class test(unittest.TestCase):

            def runTest(self):
                assert url_normalize(original) == normalized, (original, normalized, url_normalize(original))
        return test()

    for (original, normalized) in tests2.items():
        suite.addTest(testcase2(original, normalized))

    """ execute tests """
    unittest.TextTestRunner().run(suite)
