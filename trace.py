
from contextlib import contextmanager
from functools import wraps
import logging

logger = logging.getLogger(__name__)

INDENTION = 0
LEVELS = list((None,) * 5)
MAX_LENGTH = 100

@contextmanager
def indent(func, *args, **kwargs):
    global LEVELS

    values = []
    class_name = args[0].__class__.__name__ if args else ''

    # Format args
    for arg in map(str, args[1:]):
        values.append("'{}'".format(arg if len(arg) < MAX_LENGTH else arg[:MAX_LENGTH] + ' ... '))

    # Format kwargs
    for k,v in kwargs.items():
        if k == 'self':
            class_name = v.__class__.__name__
            continue
        values.append("{0}='{1}'".format(k,
            str(v) if len(str(v)) < MAX_LENGTH else str(v)[:MAX_LENGTH] + ' ... '))

    # Format the line
    str_line = ' '.join(values)

    name = class_name + '.' + func.__name__ if class_name \
        else func.__name__

    # Find the next level
    for idx, val in enumerate(LEVELS):
        if val is False or val is None:
            break

    # If the current level is False, this indicates that the level has
    # never been closed.  Print closing slash plus an addition line
    # to indicate a new function call from the previous level
    if LEVELS[idx] == False:
        logger.debug('|  ' * (idx-1) + '| /')
        logger.debug('|  ' * (idx-1) + '-')

    # Set the current level to true
    LEVELS[idx] = True

    # If we are at the end of the list, append None
    if len(LEVELS) ==  idx + 1:
        LEVELS.append(None)

    # Calculate the padding
    padding = '|  ' * idx

    # If idx is greater than 0, print the forward slash
    if idx > 0:
        logger.debug(padding[:-1] + '\\')

    logger.debug('{}* BEGIN: {} {}'.format(padding, name, str_line))

    yield

    # Set the current level to False to indicate this level has completed
    LEVELS[idx] = False

    # If the previous level has not been closed (i.e. set to None), close it
    if LEVELS[idx + 1] is not None:
        logger.debug(padding + '| /')

        # Set the previous level to None to indicate it has been closed
        LEVELS[idx+1] = None

    # Special case: if this is the last level, artifically set the level
    # to closed, since we never close the last level
    if idx == 0:
        LEVELS[idx] = None

    logger.debug('{}* END:   {} {}'.format(padding, name, str_line))

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if __debug__:
            with indent(func, *args, **kwargs):
                results = func(*args, **kwargs)
        else:
            results = func(*args, **kwargs)
        return results
    return wrapper