from typing import Optional, Dict, Any

# Global cache dictionary for simple in-memory caching
_global_cache = {}

class UserCache:
    def __init__(self):
        self._cache = _global_cache

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        pass

    async def get_user_token(self, user_id: int) -> Optional[str]:
        return self._cache.get(f"token_{user_id}")

    async def set_user_token(self, user_id: int, token: str):
        self._cache[f"token_{user_id}"] = token

    async def get_user_mode(self, user_id: int) -> Optional[str]:
        return self._cache.get(f"mode_{user_id}")

    async def set_user_mode(self, user_id: int, mode: str):
        self._cache[f"mode_{user_id}"] = mode

    async def get_user_provider(self, user_id: int) -> Optional[str]:
        return self._cache.get(f"provider_{user_id}")

    async def set_user_provider(self, user_id: int, provider: Optional[str]):
        self._cache[f"provider_{user_id}"] = provider

    async def increment_rate_limit(self, user_id: int, window: int) -> int:
        key = f"rate_{user_id}"
        count = self._cache.get(key, 0) + 1
        self._cache[key] = count
        return count

    async def set_user_data(self, user_id: int, data: Dict[str, Any], ttl: int):
        self._cache[f"data_{user_id}"] = data
