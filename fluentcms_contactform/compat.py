"""
Utils for backwards compatibility
"""

try:
    from functions import lru_cache  # Python 3.2 and up
except ImportError:
    try:
        from django.utils.lru_cache import lru_cache  # Django 1.7
    except ImportError:
        from django.utils.functional import memoize  # Django 1.6

        def lru_cache():
            CACHE = {}

            def _dec(func):
                func = memoize(func, CACHE, 1)
                return func
            return _dec
