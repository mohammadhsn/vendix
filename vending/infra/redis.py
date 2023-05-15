from typing import Optional

import redis


_redis_client: Optional[redis.Redis] = None


def redis_client() -> redis.Redis:
    global _redis_client
    if _redis_client is not None:
        return _redis_client

    _redis_client = redis.Redis(host='redis',
                                port=6379,
                                db=0)

    return redis_client()
