#!/usr/bin/env python3
"""
Performance Optimization Service
Provides caching, parallelization, streaming, and monitoring for API performance

Features:
- ElastiCache integration for distributed caching
- Request parallelization for MCP queries
- Response streaming for immediate feedback
- Query result caching with TTL
- Performance monitoring and metrics collection
"""

import asyncio
import hashlib
import json
import time
from typing import Any, Dict, List, Optional, Callable, Awaitable, AsyncGenerator
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import logging
import os

logger = logging.getLogger(__name__)


class CacheStrategy(str, Enum):
    """Cache strategy types"""
    MEMORY = "memory"
    ELASTICACHE = "elasticache"
    HYBRID = "hybrid"


class StreamingMode(str, Enum):
    """Streaming response modes"""
    NONE = "none"
    CHUNKS = "chunks"
    LINES = "lines"
    JSON = "json"


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    key: str
    value: Any
    created_at: datetime
    ttl_seconds: int
    hit_count: int = 0
    last_accessed: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        if self.ttl_seconds <= 0:
            return False
        expiry_time = self.created_at + timedelta(seconds=self.ttl_seconds)
        return datetime.now() > expiry_time
    
    def access(self):
        """Record cache access"""
        self.hit_count += 1
        self.last_accessed = datetime.now()


@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    request_count: int = 0
    cache_hits: int = 0
    cache_misses: int = 0
    total_response_time: float = 0.0
    min_response_time: float = float('inf')
    max_response_time: float = 0.0
    parallel_requests: int = 0
    streaming_requests: int = 0
    errors: int = 0
    
    @property
    def cache_hit_rate(self) -> float:
        """Calculate cache hit rate"""
        total = self.cache_hits + self.cache_misses
        return (self.cache_hits / total * 100) if total > 0 else 0.0
    
    @property
    def avg_response_time(self) -> float:
        """Calculate average response time"""
        return (self.total_response_time / self.request_count) if self.request_count > 0 else 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary"""
        return {
            'request_count': self.request_count,
            'cache_hits': self.cache_hits,
            'cache_misses': self.cache_misses,
            'cache_hit_rate': round(self.cache_hit_rate, 2),
            'avg_response_time_ms': round(self.avg_response_time * 1000, 2),
            'min_response_time_ms': round(self.min_response_time * 1000, 2) if self.min_response_time != float('inf') else 0,
            'max_response_time_ms': round(self.max_response_time * 1000, 2),
            'parallel_requests': self.parallel_requests,
            'streaming_requests': self.streaming_requests,
            'errors': self.errors
        }


class ElastiCacheClient:
    """
    ElastiCache Redis client wrapper
    Falls back to in-memory cache if ElastiCache is unavailable
    """
    
    def __init__(self, redis_endpoint: Optional[str] = None, redis_port: int = 6379):
        self.redis_endpoint = redis_endpoint or os.getenv("ELASTICACHE_ENDPOINT")
        self.redis_port = redis_port
        self.redis_client = None
        self.fallback_cache = None
        self._initialized = False
        
    async def initialize(self):
        """Initialize Redis connection"""
        if self._initialized:
            return
            
        try:
            # Try to import redis
            import redis.asyncio as aioredis
            
            if self.redis_endpoint:
                self.redis_client = await aioredis.from_url(
                    f"redis://{self.redis_endpoint}:{self.redis_port}",
                    encoding="utf-8",
                    decode_responses=True,
                    socket_connect_timeout=2,
                    socket_timeout=2
                )
                # Test connection
                await self.redis_client.ping()
                logger.info(f"Connected to ElastiCache at {self.redis_endpoint}")
            else:
                logger.warning("ElastiCache endpoint not configured, using in-memory fallback")
                self.fallback_cache = InMemoryCache(max_size=1000)
                
        except ImportError:
            logger.warning("redis package not installed, using in-memory fallback")
            self.fallback_cache = InMemoryCache(max_size=1000)
        except Exception as e:
            logger.warning(f"Failed to connect to ElastiCache: {e}, using in-memory fallback")
            self.fallback_cache = InMemoryCache(max_size=1000)
        
        self._initialized = True
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self._initialized:
            await self.initialize()
            
        try:
            if self.redis_client:
                value = await self.redis_client.get(key)
                if value:
                    return json.loads(value)
                return None
            else:
                return await self.fallback_cache.get(key)
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            return None
    
    async def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value in cache"""
        if not self._initialized:
            await self.initialize()
            
        try:
            if self.redis_client:
                await self.redis_client.setex(
                    key,
                    ttl_seconds,
                    json.dumps(value)
                )
            else:
                await self.fallback_cache.set(key, value, ttl_seconds)
        except Exception as e:
            logger.error(f"Cache set error: {e}")
    
    async def delete(self, key: str):
        """Delete value from cache"""
        if not self._initialized:
            await self.initialize()
            
        try:
            if self.redis_client:
                await self.redis_client.delete(key)
            else:
                await self.fallback_cache.delete(key)
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
    
    async def clear(self):
        """Clear all cache entries"""
        if not self._initialized:
            await self.initialize()
            
        try:
            if self.redis_client:
                await self.redis_client.flushdb()
            else:
                await self.fallback_cache.clear()
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        if self.redis_client:
            return {
                'type': 'elasticache',
                'endpoint': self.redis_endpoint,
                'status': 'connected'
            }
        elif self.fallback_cache:
            stats = self.fallback_cache.get_stats()
            stats['type'] = 'in-memory-fallback'
            return stats
        else:
            return {'type': 'not-initialized', 'status': 'pending'}


class InMemoryCache:
    """In-memory cache implementation"""
    
    def __init__(self, max_size: int = 1000):
        self.cache: Dict[str, CacheEntry] = {}
        self.max_size = max_size
        self._lock = asyncio.Lock()
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        async with self._lock:
            entry = self.cache.get(key)
            if entry and not entry.is_expired():
                entry.access()
                return entry.value
            elif entry:
                # Remove expired entry
                del self.cache[key]
            return None
    
    async def set(self, key: str, value: Any, ttl_seconds: int = 300):
        """Set value in cache"""
        async with self._lock:
            # Evict oldest entries if cache is full
            if len(self.cache) >= self.max_size:
                await self._evict_lru()
            
            self.cache[key] = CacheEntry(
                key=key,
                value=value,
                created_at=datetime.now(),
                ttl_seconds=ttl_seconds
            )
    
    async def delete(self, key: str):
        """Delete value from cache"""
        async with self._lock:
            if key in self.cache:
                del self.cache[key]
    
    async def clear(self):
        """Clear all cache entries"""
        async with self._lock:
            self.cache.clear()
    
    async def _evict_lru(self):
        """Evict least recently used entry"""
        if not self.cache:
            return
        
        # Find entry with oldest last_accessed time
        lru_key = min(
            self.cache.keys(),
            key=lambda k: self.cache[k].last_accessed or self.cache[k].created_at
        )
        del self.cache[lru_key]
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_hits = sum(entry.hit_count for entry in self.cache.values())
        return {
            'size': len(self.cache),
            'max_size': self.max_size,
            'total_hits': total_hits,
            'entries': len(self.cache)
        }


class PerformanceService:
    """
    Performance optimization service with caching, parallelization, and monitoring
    
    Features:
    - ElastiCache integration with automatic fallback
    - MCP query parallelization with concurrency control
    - Response streaming for real-time feedback
    - Intelligent caching with TTL management
    - Comprehensive performance metrics
    """
    
    def __init__(
        self,
        cache_strategy: CacheStrategy = CacheStrategy.HYBRID,
        default_ttl: int = 300,
        enable_metrics: bool = True,
        elasticache_endpoint: Optional[str] = None
    ):
        self.cache_strategy = cache_strategy
        self.default_ttl = default_ttl
        self.enable_metrics = enable_metrics
        
        # Initialize caches based on strategy
        self.memory_cache = InMemoryCache(max_size=1000)
        self.elasticache = None
        
        if cache_strategy in [CacheStrategy.ELASTICACHE, CacheStrategy.HYBRID]:
            self.elasticache = ElastiCacheClient(redis_endpoint=elasticache_endpoint)
        
        # Initialize metrics
        self.metrics = PerformanceMetrics()
        
        logger.info(f"Performance service initialized with {cache_strategy} cache")
    
    def _generate_cache_key(self, prefix: str, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = f"{prefix}:{json.dumps(args, sort_keys=True)}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    async def _get_from_cache(self, cache_key: str) -> Optional[Any]:
        """Get value from cache based on strategy"""
        if self.cache_strategy == CacheStrategy.MEMORY:
            return await self.memory_cache.get(cache_key)
        elif self.cache_strategy == CacheStrategy.ELASTICACHE and self.elasticache:
            return await self.elasticache.get(cache_key)
        elif self.cache_strategy == CacheStrategy.HYBRID:
            # Try memory first (faster)
            value = await self.memory_cache.get(cache_key)
            if value is not None:
                return value
            # Fall back to ElastiCache
            if self.elasticache:
                value = await self.elasticache.get(cache_key)
                if value is not None:
                    # Promote to memory cache
                    await self.memory_cache.set(cache_key, value, self.default_ttl)
                return value
        return None
    
    async def _set_in_cache(self, cache_key: str, value: Any, ttl: int):
        """Set value in cache based on strategy"""
        if self.cache_strategy == CacheStrategy.MEMORY:
            await self.memory_cache.set(cache_key, value, ttl)
        elif self.cache_strategy == CacheStrategy.ELASTICACHE and self.elasticache:
            await self.elasticache.set(cache_key, value, ttl)
        elif self.cache_strategy == CacheStrategy.HYBRID:
            # Store in both caches
            await self.memory_cache.set(cache_key, value, ttl)
            if self.elasticache:
                await self.elasticache.set(cache_key, value, ttl)
    
    async def cached_call(
        self,
        func: Callable[..., Awaitable[Any]],
        cache_key_prefix: str,
        ttl_seconds: Optional[int] = None,
        *args,
        **kwargs
    ) -> Any:
        """
        Execute function with caching
        
        Args:
            func: Async function to execute
            cache_key_prefix: Prefix for cache key
            ttl_seconds: Cache TTL (uses default if None)
            *args, **kwargs: Arguments for function
        
        Returns:
            Function result (cached or fresh)
        """
        start_time = time.time()
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        
        # Generate cache key
        cache_key = self._generate_cache_key(cache_key_prefix, *args, **kwargs)
        
        # Try to get from cache
        cached_value = await self._get_from_cache(cache_key)
        
        if cached_value is not None:
            # Cache hit
            if self.enable_metrics:
                self.metrics.cache_hits += 1
                self.metrics.request_count += 1
                response_time = time.time() - start_time
                self.metrics.total_response_time += response_time
                self.metrics.min_response_time = min(self.metrics.min_response_time, response_time)
                self.metrics.max_response_time = max(self.metrics.max_response_time, response_time)
            
            logger.debug(f"Cache hit for key: {cache_key}")
            return cached_value
        
        # Cache miss - execute function
        if self.enable_metrics:
            self.metrics.cache_misses += 1
        
        logger.debug(f"Cache miss for key: {cache_key}")
        
        try:
            result = await func(*args, **kwargs)
            
            # Store in cache
            await self._set_in_cache(cache_key, result, ttl)
            
            # Update metrics
            if self.enable_metrics:
                self.metrics.request_count += 1
                response_time = time.time() - start_time
                self.metrics.total_response_time += response_time
                self.metrics.min_response_time = min(self.metrics.min_response_time, response_time)
                self.metrics.max_response_time = max(self.metrics.max_response_time, response_time)
            
            return result
            
        except Exception as e:
            if self.enable_metrics:
                self.metrics.errors += 1
            logger.error(f"Error in cached call: {e}")
            raise
    
    async def parallel_execute(
        self,
        tasks: List[Callable[..., Awaitable[Any]]],
        max_concurrent: int = 10,
        timeout_seconds: Optional[float] = None
    ) -> List[Any]:
        """
        Execute multiple tasks in parallel with concurrency limit
        
        Optimized for MCP queries with timeout and error handling
        
        Args:
            tasks: List of async functions to execute
            max_concurrent: Maximum concurrent tasks
            timeout_seconds: Optional timeout for each task
        
        Returns:
            List of results in same order as tasks
        """
        if self.enable_metrics:
            self.metrics.parallel_requests += len(tasks)
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def bounded_task(task, index):
            async with semaphore:
                try:
                    if timeout_seconds:
                        return await asyncio.wait_for(task(), timeout=timeout_seconds)
                    else:
                        return await task()
                except asyncio.TimeoutError:
                    logger.warning(f"Task {index} timed out after {timeout_seconds}s")
                    return None
                except Exception as e:
                    logger.error(f"Task {index} failed: {e}")
                    return e
        
        results = await asyncio.gather(
            *[bounded_task(task, i) for i, task in enumerate(tasks)],
            return_exceptions=False
        )
        
        # Count errors
        error_count = sum(1 for r in results if isinstance(r, Exception))
        if self.enable_metrics and error_count > 0:
            self.metrics.errors += error_count
        
        return results
    
    async def parallel_mcp_queries(
        self,
        mcp_queries: List[Dict[str, Any]],
        max_concurrent: int = 5,
        cache_results: bool = True,
        cache_ttl: int = 300
    ) -> List[Dict[str, Any]]:
        """
        Execute multiple MCP queries in parallel with caching
        
        Optimized for querying multiple MCP servers simultaneously
        
        Args:
            mcp_queries: List of MCP query configs with 'mcp_name', 'query', 'params'
            max_concurrent: Maximum concurrent MCP queries
            cache_results: Whether to cache results
            cache_ttl: Cache TTL in seconds
        
        Returns:
            List of MCP query results
        """
        async def execute_mcp_query(query_config: Dict[str, Any]) -> Dict[str, Any]:
            mcp_name = query_config.get('mcp_name', 'unknown')
            query = query_config.get('query', '')
            params = query_config.get('params', {})
            
            # Generate cache key if caching enabled
            if cache_results:
                cache_key = self._generate_cache_key(
                    f"mcp_{mcp_name}",
                    query,
                    **params
                )
                
                # Check cache
                cached_result = await self._get_from_cache(cache_key)
                if cached_result is not None:
                    logger.debug(f"MCP cache hit: {mcp_name}")
                    return {
                        'mcp_name': mcp_name,
                        'result': cached_result,
                        'cached': True
                    }
            
            # Execute query (placeholder - integrate with actual MCP client)
            try:
                # This would call the actual MCP service
                result = {
                    'mcp_name': mcp_name,
                    'query': query,
                    'data': f"Result from {mcp_name}",
                    'timestamp': datetime.now().isoformat()
                }
                
                # Cache result
                if cache_results:
                    await self._set_in_cache(cache_key, result, cache_ttl)
                
                return {
                    'mcp_name': mcp_name,
                    'result': result,
                    'cached': False
                }
                
            except Exception as e:
                logger.error(f"MCP query failed for {mcp_name}: {e}")
                return {
                    'mcp_name': mcp_name,
                    'error': str(e),
                    'cached': False
                }
        
        # Create tasks
        tasks = [lambda q=q: execute_mcp_query(q) for q in mcp_queries]
        
        # Execute in parallel
        results = await self.parallel_execute(
            tasks,
            max_concurrent=max_concurrent,
            timeout_seconds=10.0
        )
        
        return results
    
    async def stream_response(
        self,
        generator: AsyncGenerator[Any, None],
        mode: StreamingMode = StreamingMode.CHUNKS,
        buffer_size: int = 1024
    ) -> AsyncGenerator[Any, None]:
        """
        Stream response with buffering and error handling
        
        Args:
            generator: Async generator that yields data
            mode: Streaming mode (chunks, lines, json)
            buffer_size: Buffer size for chunking
        
        Yields:
            Streamed data chunks
        """
        if self.enable_metrics:
            self.metrics.streaming_requests += 1
        
        buffer = []
        buffer_bytes = 0
        
        try:
            async for chunk in generator:
                if mode == StreamingMode.CHUNKS:
                    # Stream raw chunks
                    yield chunk
                    
                elif mode == StreamingMode.LINES:
                    # Buffer and stream complete lines
                    buffer.append(chunk)
                    if '\n' in chunk:
                        yield ''.join(buffer)
                        buffer = []
                        
                elif mode == StreamingMode.JSON:
                    # Buffer and stream complete JSON objects
                    buffer.append(chunk)
                    combined = ''.join(buffer)
                    try:
                        # Try to parse as JSON
                        json.loads(combined)
                        yield combined
                        buffer = []
                    except json.JSONDecodeError:
                        # Not complete yet, continue buffering
                        pass
                        
                else:
                    # Default: stream as-is
                    yield chunk
            
            # Flush remaining buffer
            if buffer:
                yield ''.join(buffer)
                
        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            if self.enable_metrics:
                self.metrics.errors += 1
            raise
    
    async def stream_with_cache(
        self,
        generator: AsyncGenerator[Any, None],
        cache_key: str,
        ttl_seconds: int = 300
    ) -> AsyncGenerator[Any, None]:
        """
        Stream response while caching the complete result
        
        Args:
            generator: Async generator that yields chunks
            cache_key: Cache key for storing complete result
            ttl_seconds: Cache TTL
        
        Yields:
            Streamed chunks
        """
        accumulated = []
        
        try:
            async for chunk in generator:
                accumulated.append(chunk)
                yield chunk
            
            # Cache complete result
            complete_result = ''.join(str(c) for c in accumulated)
            await self._set_in_cache(cache_key, complete_result, ttl_seconds)
            
        except Exception as e:
            logger.error(f"Error in stream_with_cache: {e}")
            raise
    
    async def invalidate_cache(self, cache_key_prefix: str, *args, **kwargs):
        """Invalidate specific cache entry"""
        cache_key = self._generate_cache_key(cache_key_prefix, *args, **kwargs)
        
        if self.cache_strategy == CacheStrategy.MEMORY:
            await self.memory_cache.delete(cache_key)
        elif self.cache_strategy == CacheStrategy.ELASTICACHE and self.elasticache:
            await self.elasticache.delete(cache_key)
        elif self.cache_strategy == CacheStrategy.HYBRID:
            await self.memory_cache.delete(cache_key)
            if self.elasticache:
                await self.elasticache.delete(cache_key)
        
        logger.debug(f"Cache invalidated for key: {cache_key}")
    
    async def clear_cache(self):
        """Clear all cache entries"""
        if self.cache_strategy == CacheStrategy.MEMORY:
            await self.memory_cache.clear()
        elif self.cache_strategy == CacheStrategy.ELASTICACHE and self.elasticache:
            await self.elasticache.clear()
        elif self.cache_strategy == CacheStrategy.HYBRID:
            await self.memory_cache.clear()
            if self.elasticache:
                await self.elasticache.clear()
        
        logger.info("Cache cleared")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get performance metrics"""
        cache_stats = {}
        
        if self.cache_strategy == CacheStrategy.MEMORY:
            cache_stats = self.memory_cache.get_stats()
        elif self.cache_strategy == CacheStrategy.ELASTICACHE and self.elasticache:
            cache_stats = self.elasticache.get_stats()
        elif self.cache_strategy == CacheStrategy.HYBRID:
            cache_stats = {
                'memory': self.memory_cache.get_stats(),
                'elasticache': self.elasticache.get_stats() if self.elasticache else None
            }
        
        return {
            'performance': self.metrics.to_dict(),
            'cache': cache_stats,
            'cache_strategy': self.cache_strategy.value
        }
    
    def reset_metrics(self):
        """Reset performance metrics"""
        self.metrics = PerformanceMetrics()
        logger.info("Metrics reset")
    
    async def warmup_cache(self, warmup_queries: List[Dict[str, Any]]):
        """
        Warm up cache with common queries
        
        Args:
            warmup_queries: List of query configs to pre-cache
        """
        logger.info(f"Warming up cache with {len(warmup_queries)} queries")
        
        async def execute_warmup(query_config):
            try:
                func = query_config.get('func')
                cache_key = query_config.get('cache_key')
                ttl = query_config.get('ttl', self.default_ttl)
                args = query_config.get('args', [])
                kwargs = query_config.get('kwargs', {})
                
                if func and cache_key:
                    await self.cached_call(func, cache_key, ttl, *args, **kwargs)
            except Exception as e:
                logger.warning(f"Warmup query failed: {e}")
        
        # Execute warmup queries in parallel
        tasks = [lambda q=q: execute_warmup(q) for q in warmup_queries]
        await self.parallel_execute(tasks, max_concurrent=10)


# Singleton instance
_performance_service: Optional[PerformanceService] = None


def get_performance_service() -> PerformanceService:
    """Get or create performance service singleton"""
    global _performance_service
    if _performance_service is None:
        # Use HYBRID strategy for best performance (memory + ElastiCache)
        # Falls back to memory-only if ElastiCache unavailable
        _performance_service = PerformanceService(
            cache_strategy=CacheStrategy.HYBRID,
            default_ttl=300,  # 5 minutes
            enable_metrics=True,
            elasticache_endpoint=os.getenv("ELASTICACHE_ENDPOINT")
        )
    return _performance_service


# Decorator for easy caching
def cached(cache_key_prefix: str, ttl_seconds: int = 300):
    """
    Decorator for caching async function results
    
    Usage:
        @cached("my_function", ttl_seconds=600)
        async def my_function(arg1, arg2):
            return result
    """
    def decorator(func: Callable[..., Awaitable[Any]]):
        async def wrapper(*args, **kwargs):
            service = get_performance_service()
            return await service.cached_call(func, cache_key_prefix, ttl_seconds, *args, **kwargs)
        return wrapper
    return decorator
