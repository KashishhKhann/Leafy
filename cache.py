"""
Response caching system for Leafy
Caches Wikipedia, calculations, news, and other API responses
"""

import hashlib
import json
from typing import Optional, Any
from db import db
from logger import log_info, log_error


class ResponseCache:
    """Cache API responses with TTL support."""
    
    # Cache TTLs in seconds
    TTL_WIKIPEDIA = 7 * 24 * 3600  # 7 days
    TTL_CALCULATION = 30 * 24 * 3600  # 30 days
    TTL_NEWS = 24 * 3600  # 1 day
    TTL_SHORT = 3600  # 1 hour
    
    @staticmethod
    def hash_query(query: str, query_type: str) -> str:
        """Generate hash for query."""
        combined = f"{query_type}:{query.lower().strip()}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    @staticmethod
    def cache_result(query: str, result: str, query_type: str = "general", 
                    ttl: int = TTL_SHORT) -> bool:
        """Cache a result."""
        try:
            query_hash = ResponseCache.hash_query(query, query_type)
            
            # Convert result to string if needed
            if isinstance(result, (dict, list)):
                result = json.dumps(result)
            else:
                result = str(result)
            
            success = db.cache_response(query_hash, query_type, result, ttl)
            if success:
                log_info(f"Cached {query_type}: {query[:50]}")
            return success
        except Exception as e:
            log_error("CACHE", f"Failed to cache result for {query_type}", str(e))
            return False
    
    @staticmethod
    def get_cached(query: str, query_type: str = "general") -> Optional[str]:
        """Get cached result."""
        try:
            query_hash = ResponseCache.hash_query(query, query_type)
            cached = db.get_cached_response(query_hash)
            
            if cached:
                log_info(f"Cache hit for {query_type}: {query[:50]}")
                return cached
            
            return None
        except Exception as e:
            log_error("CACHE", f"Failed to retrieve cached result for {query_type}", str(e))
            return None
    
    @staticmethod
    def clear_expired() -> int:
        """Clear expired cache entries."""
        try:
            count = db.clear_expired_cache()
            if count > 0:
                log_info(f"Cleared {count} expired cache entries")
            return count
        except Exception as e:
            log_error("CACHE", "Failed to clear expired cache", str(e))
            return 0
    
    @staticmethod
    def clear_all() -> int:
        """Clear all cache."""
        try:
            count = db.clear_all_cache()
            log_info(f"Cleared all {count} cache entries")
            return count
        except Exception as e:
            log_error("CACHE", "Failed to clear all cache", str(e))
            return 0


def get_cached_or_fetch(query: str, query_type: str, 
                       fetch_func, ttl: int = ResponseCache.TTL_SHORT) -> Optional[Any]:
    """
    Get from cache or fetch fresh data.
    
    Args:
        query: Search query
        query_type: Type of query (wikipedia, calculation, news, etc.)
        fetch_func: Function that fetches fresh data
        ttl: Time to live in seconds
    
    Returns:
        Cached or fresh result
    """
    try:
        # Check cache first
        cached = ResponseCache.get_cached(query, query_type)
        if cached:
            try:
                return json.loads(cached)
            except:
                return cached
        
        # Fetch fresh data
        result = fetch_func()
        if result:
            ResponseCache.cache_result(query, result, query_type, ttl)
        
        return result
    except Exception as e:
        log_error("CACHE", f"Error in get_cached_or_fetch for {query_type}", str(e))
        return None
