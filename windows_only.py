# utils/windows_only.py

from functools import wraps
import logging
import platform

logger = logging.getLogger(__name__)

def windows_only(func):
    '''A decorator that ensures a method is only invoked on a Windows system.
    If a caller attempts to invoke the method on an operating system other
    than Windows, a NotImplementedError will be raised
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'windows' not in platform.platform().lower():
            logger.debug("Method '{}' invoked on '{}' operating system".format(
                func.__name__,
                platform.platform()))
            raise NotImplementedError('Only Windows is supported')
        return func(*args, **kwargs)
    return wrapper