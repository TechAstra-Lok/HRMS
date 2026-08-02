"""Rate limiting implementation."""

import os
from typing import Optional, Tuple

import redis


class RateLimiter:
    """A simple Redis-backed rate limiter with graceful fallback behavior."""

    def __init__(self, redis_url: Optional[str] = None):
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.default_limit = os.getenv('RATE_LIMIT_DEFAULT', '100/hour')
        self.redis = None
        try:
            self.redis = redis.Redis.from_url(self.redis_url, decode_responses=True)
            self.redis.ping()
        except Exception:
            self.redis = None

    def is_allowed(self, key: str, limit: Optional[str] = None) -> Tuple[bool, int, int]:
        """Check whether the provided key is still within the allowed request count."""
        limit = limit or self.default_limit
        if '/' in limit:
            max_requests, time_window = limit.split('/', 1)
            max_requests = int(max_requests)
            if 'second' in time_window:
                seconds = 1
            elif 'minute' in time_window:
                seconds = 60
            elif 'hour' in time_window:
                seconds = 3600
            elif 'day' in time_window:
                seconds = 86400
            else:
                seconds = 3600
        else:
            max_requests = int(limit)
            seconds = 3600

        redis_key = f'rate_limit:{key}'
        if self.redis is None:
            return True, max_requests, seconds

        try:
            current = self.redis.get(redis_key)
            if current is None:
                self.redis.setex(redis_key, seconds, 1)
                return True, max_requests - 1, seconds

            current = int(current)
            if current >= max_requests:
                ttl = self.redis.ttl(redis_key)
                return False, 0, ttl if ttl > 0 else seconds

            self.redis.incr(redis_key)
            return True, max_requests - current - 1, seconds
        except Exception:
            return True, max_requests, seconds

    def get_remaining(self, key: str) -> int:
        """Return the remaining requests for a key when Redis is available."""
        if self.redis is None:
            return 0
        try:
            current = self.redis.get(f'rate_limit:{key}')
            if current is None:
                return 0
            return int(current)
        except Exception:
            return 0

    def reset(self, key: str) -> None:
        """Reset the rate limit counter for a key."""
        if self.redis is None:
            return
        try:
            self.redis.delete(f'rate_limit:{key}')
        except Exception:
            return


rate_limiter = RateLimiter()
