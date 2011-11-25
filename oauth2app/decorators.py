#-*- coding: utf-8 -*-

import functools, inspect


def decorator(func):
    """ Allow to use decorator either with arguments or not. 
    See http://wiki.python.org/moin/PythonDecoratorLibrary#Creating_decorator_with_optional_arguments
    """

    def isFuncArg(*args, **kw):
        return len(args) == 1 and len(kw) == 0 and (
            inspect.isfunction(args[0]) or isinstance(args[0], type))

    if isinstance(func, type):
        def class_wrapper(*args, **kw):
            if isFuncArg(*args, **kw):
                return func()(*args, **kw) # create class before usage
            return func(*args, **kw)
        class_wrapper.__name__ = func.__name__
        class_wrapper.__module__ = func.__module__
        return class_wrapper

    @functools.wraps(func)
    def func_wrapper(*args, **kw):
        if isFuncArg(*args, **kw):
            return func(*args, **kw)

        def functor(userFunc):
            return func(userFunc, *args, **kw)

        return functor

    return func_wrapper


@decorator
def authenticate(func, *args, **kw):
    """Authenticate a request with no scope."""
    raise NotImplementedError()
    return func(*args, **kw)


@decorator
class authenticate(object):
    """Authenticate a request with scope."""
    def __init__(self, *args, **kw):
        self.args = args
        self.kw   = kw

    def __call__(self, func):
        raise NotImplementedError()
        return func(*self.args, **self.kw)
