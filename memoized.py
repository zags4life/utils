# memoized.py
from functools import wraps

import logging
logger = logging.getLogger(__name__)

def memoized(func):
    """Decorator that caches a functions return value each time it is called.
    If called later with the same arguments, the cached value is returned, and
    not re-evaluated.
    """
    cache = {}
    @wraps(func)
    def memo(*args, **kwargs):
        hash_value = 0
        # hash together kwargs
        for pair in kwargs.items():
            hash_value ^= hash(pair)

        # hash together args with value and return
        hash_value ^= hash(args)

        try:
            val = cache[hash_value]
            logger.debug("Using cached value of function '{0}' "\
                "(hash: {1:X})".format(func.__name__, hash_value))
            return val
        except KeyError:
            value = func(*args, **kwargs)
            cache[hash_value] = value
            logger.debug("Caching value of function '{0}' "\
                "(hash: {1:X})".format(func.__name__, hash_value))
            return value
        except TypeError:
            # uncacheable -- for instance, passing a list as an argument.
            # Better to not cache than to blow up entirely.
            logger.warning("Uncachable function '{0}'".format(func.__name__))
            return func(*args, **kwargs)
    return memo