# cache_util.py - simple in-memory cache with TTL (generated)
"""Cache utility: in-memory get/set with TTL. For Redis, set CACHE_REDIS_URL in config."""
import os
import time
import functools

_USE_REDIS = os.getenv("CACHE_REDIS_URL", "").strip() != ""
_MEMORY_CACHE = {}
_MEMORY_CACHE_TIME = {}
_DEFAULT_TTL = int(os.getenv("CACHE_TTL_SECONDS", "300"))


def get(key: str):
    """Get value by key. Returns None if missing or expired."""
    if _USE_REDIS:
        try:
            import redis
            r = redis.from_url(os.getenv("CACHE_REDIS_URL"))
            return r.get(key)
        except Exception:
            return None
    if key not in _MEMORY_CACHE:
        return None
    ttl = _MEMORY_CACHE_TIME.get(key, 0)
    if ttl and time.time() > ttl:
        _MEMORY_CACHE.pop(key, None)
        _MEMORY_CACHE_TIME.pop(key, None)
        return None
    return _MEMORY_CACHE.get(key)


def set(key: str, value, ttl_seconds: int = None):
    """Set value with optional TTL (seconds)."""
    ttl_seconds = ttl_seconds or _DEFAULT_TTL
    if _USE_REDIS:
        try:
            import redis
            r = redis.from_url(os.getenv("CACHE_REDIS_URL"))
            r.setex(key, ttl_seconds, str(value) if not isinstance(value, (str, bytes)) else value)
        except Exception:
            pass
        return
    _MEMORY_CACHE[key] = value
    _MEMORY_CACHE_TIME[key] = time.time() + ttl_seconds if ttl_seconds else 0


def cache_ttl(ttl_seconds: int = None):
    """Decorator: cache function result with TTL. Key = function name + str(args) + str(kwargs)."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = f"{func.__module__}.{func.__name__}:{args!r}:{sorted(kwargs.items())!r}"
            v = get(key)
            if v is not None:
                return v
            v = func(*args, **kwargs)
            set(key, v, ttl_seconds or _DEFAULT_TTL)
            return v
        return wrapper
    return decorator
