import redis
from pkg.config import config


_pool = None


def create_client() -> redis.Redis:
    global _pool
    if _pool is None:
        _pool = redis.ConnectionPool.from_url(config.redis_uri)

    return redis.Redis(connection_pool=_pool)
