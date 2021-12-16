"""
cached function for given function by Uliana Eskova
"""
from functools import wraps


def cached_function(func):
    """
    cached function
    """
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        now_all_args = ()
        for arg in args:
            if arg not in now_all_args:
                now_all_args += tuple(str(arg))
        now_all_args += tuple(kwargs.items())
        if now_all_args not in cache.keys():
            cache[now_all_args] = func(*args, **kwargs)
        return cache[now_all_args]

    return wrapper
