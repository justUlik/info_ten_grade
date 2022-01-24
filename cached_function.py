"""
cached function and lru cached function for given function by Uliana Eskova
"""
from functools import wraps
from collections import OrderedDict


def lru_cached_function(cache_size):
    """
    lru cached function
    """
    if type(cache_size) != int:
        raise TypeError('cache_size must be int not {}'.format(type(cache_size).__name__))
    if cache_size <= 0:
        raise TypeError('cache_size must be positive')
    cache = OrderedDict()

    def wrapper(func):
        @wraps(func)
        def called(*args, **kwargs):
            now_all_args = ()
            for arg in args:
                if arg not in now_all_args:
                    now_all_args += tuple(str(arg))
            now_all_args += tuple(set(kwargs.items()))
            try:
                cache.move_to_end(now_all_args)
            except KeyError:
                if len(cache) == cache_size:
                    cache.popitem(last=False)
                cache[now_all_args] = func(*args, **kwargs)
            return cache[now_all_args]
        return called
    return wrapper


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
