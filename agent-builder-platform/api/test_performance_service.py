#!/usr/bin/env python3
"""
Test suite for Performance Service
Tests caching, parallelization, streaming, and metrics

Covers:
- ElastiCache integration with fallback
- MCP query parallelization
- Response streaming
- Query result caching with TTL
- Performance monitoring and metrics
"""

import asyncio
import pytest
import time
import json
from performance_service import (
    PerformanceService, CacheStrategy, InMemoryCache,
    PerformanceMetrics, CacheEntry, cached, StreamingMode
)


class TestInMemoryCache:
    """Test in-memory cache implementation"""
    
    @pytest.mark.asyncio
    async def test_cache_set_and_get(self):
        """Test basic cache set and get operations"""
        cache = InMemoryCache(max_size=10)
        
        # Set value
        await cache.set("key1", "value1", ttl_seconds=60)
        
        # Get value
        value = await cache.get("key1")
        assert value == "value1"
    
    @pytest.mark.asyncio
    async def test_cache_expiration(self):
        """Test cache entry expiration"""
        cache = InMemoryCache(max_size=10)
        
        # Set value with 1 second TTL
        await cache.set("key1", "value1", ttl_seconds=1)
        
        # Should be available immediately
        value = await cache.get("key1")
        assert value == "value1"
        
        # Wait for expiration
        await asyncio.sleep(1.1)
        
        # Should be expired
        value = await cache.get("key1")
        assert value is None
    
    @pytest.mark.asyncio
    async def test_cache_lru_eviction(self):
        """Test LRU eviction when cache is full"""
        cache = InMemoryCache(max_size=3)
        
        # Fill cache with small delays to ensure different timestamps
        await cache.set("key1", "value1")
        await asyncio.sleep(0.01)
        await cache.set("key2", "value2")
        await asyncio.sleep(0.01)
        await cache.set("key3", "value3")
        await asyncio.sleep(0.01)
        
        # Access key1 and key3 to make them recently used
        await cache.get("key1")
        await asyncio.sleep(0.01)
        await cache.get("key3")
        await asyncio.sleep(0.01)
        
        # Add new entry (should evict key2 as least recently used)
        await cache.set("key4", "value4")
        
        # key2 should be evicted
        assert await cache.get("key2") is None
        
        # Others should still exist
        assert await cache.get("key1") == "value1"
        assert await cache.get("key3") == "value3"
        assert await cache.get("key4") == "value4"
    
    @pytest.mark.asyncio
    async def test_cache_delete(self):
        """Test cache entry deletion"""
        cache = InMemoryCache(max_size=10)
        
        await cache.set("key1", "value1")
        assert await cache.get("key1") == "value1"
        
        await cache.delete("key1")
        assert await cache.get("key1") is None
    
    @pytest.mark.asyncio
    async def test_cache_clear(self):
        """Test clearing all cache entries"""
        cache = InMemoryCache(max_size=10)
        
        await cache.set("key1", "value1")
        await cache.set("key2", "value2")
        
        await cache.clear()
        
        assert await cache.get("key1") is None
        assert await cache.get("key2") is None
        assert cache.get_stats()['size'] == 0


class TestPerformanceService:
    """Test performance service functionality"""
    
    @pytest.mark.asyncio
    async def test_cached_call_hit(self):
        """Test cached call with cache hit"""
        service = PerformanceService(enable_metrics=True)
        
        call_count = 0
        
        async def expensive_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)
            return x * 2
        
        # First call - cache miss
        result1 = await service.cached_call(
            expensive_function,
            "test_func",
            60,
            5
        )
        assert result1 == 10
        assert call_count == 1
        assert service.metrics.cache_misses == 1
        
        # Second call - cache hit
        result2 = await service.cached_call(
            expensive_function,
            "test_func",
            60,
            5
        )
        assert result2 == 10
        assert call_count == 1  # Function not called again
        assert service.metrics.cache_hits == 1
    
    @pytest.mark.asyncio
    async def test_cached_call_different_args(self):
        """Test cached call with different arguments"""
        service = PerformanceService(enable_metrics=True)
        
        call_count = 0
        
        async def expensive_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # Call with different arguments
        result1 = await service.cached_call(expensive_function, "test_func", 60, 5)
        result2 = await service.cached_call(expensive_function, "test_func", 60, 10)
        
        assert result1 == 10
        assert result2 == 20
        assert call_count == 2  # Both calls executed
        assert service.metrics.cache_misses == 2
    
    @pytest.mark.asyncio
    async def test_parallel_execute(self):
        """Test parallel task execution"""
        service = PerformanceService(enable_metrics=True)
        
        async def task(n: int) -> int:
            await asyncio.sleep(0.1)
            return n * 2
        
        # Create 5 tasks
        tasks = [lambda i=i: task(i) for i in range(5)]
        
        start_time = time.time()
        results = await service.parallel_execute(tasks, max_concurrent=5)
        elapsed = time.time() - start_time
        
        # All tasks should complete
        assert len(results) == 5
        assert results == [0, 2, 4, 6, 8]
        
        # Should take ~0.1s (parallel) not ~0.5s (sequential)
        assert elapsed < 0.3
        
        # Metrics should be updated
        assert service.metrics.parallel_requests == 5
    
    @pytest.mark.asyncio
    async def test_parallel_execute_with_errors(self):
        """Test parallel execution with some tasks failing"""
        service = PerformanceService(enable_metrics=True)
        
        async def task(n: int) -> int:
            if n == 2:
                raise ValueError("Task 2 failed")
            return n * 2
        
        tasks = [lambda i=i: task(i) for i in range(5)]
        
        results = await service.parallel_execute(tasks, max_concurrent=5)
        
        # Check results
        assert results[0] == 0
        assert results[1] == 2
        assert isinstance(results[2], ValueError)
        assert results[3] == 6
        assert results[4] == 8
        
        # Error should be counted
        assert service.metrics.errors >= 1
    
    @pytest.mark.asyncio
    async def test_cache_invalidation(self):
        """Test cache invalidation"""
        service = PerformanceService(enable_metrics=True)
        
        call_count = 0
        
        async def expensive_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call
        result1 = await service.cached_call(expensive_function, "test_func", 60, 5)
        assert result1 == 10
        assert call_count == 1
        
        # Invalidate cache
        await service.invalidate_cache("test_func", 5)
        
        # Next call should execute function again
        result2 = await service.cached_call(expensive_function, "test_func", 60, 5)
        assert result2 == 10
        assert call_count == 2
    
    @pytest.mark.asyncio
    async def test_metrics_tracking(self):
        """Test performance metrics tracking"""
        service = PerformanceService(enable_metrics=True)
        
        async def test_function(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2
        
        # Execute multiple calls
        await service.cached_call(test_function, "test", 60, 1)  # Miss
        await service.cached_call(test_function, "test", 60, 1)  # Hit
        await service.cached_call(test_function, "test", 60, 2)  # Miss
        
        metrics = service.get_metrics()
        
        assert metrics['performance']['request_count'] == 3
        assert metrics['performance']['cache_hits'] == 1
        assert metrics['performance']['cache_misses'] == 2
        assert metrics['performance']['cache_hit_rate'] == 33.33
        assert metrics['performance']['avg_response_time_ms'] > 0
    
    @pytest.mark.asyncio
    async def test_cached_decorator(self):
        """Test cached decorator"""
        call_count = 0
        
        @cached("decorated_func", ttl_seconds=60)
        async def decorated_function(x: int) -> int:
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call
        result1 = await decorated_function(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call (cached)
        result2 = await decorated_function(5)
        assert result2 == 10
        assert call_count == 1


class TestPerformanceMetrics:
    """Test performance metrics calculations"""
    
    def test_cache_hit_rate(self):
        """Test cache hit rate calculation"""
        metrics = PerformanceMetrics()
        
        metrics.cache_hits = 7
        metrics.cache_misses = 3
        
        assert metrics.cache_hit_rate == 70.0
    
    def test_avg_response_time(self):
        """Test average response time calculation"""
        metrics = PerformanceMetrics()
        
        metrics.request_count = 5
        metrics.total_response_time = 2.5
        
        assert metrics.avg_response_time == 0.5
    
    def test_metrics_to_dict(self):
        """Test metrics conversion to dictionary"""
        metrics = PerformanceMetrics()
        
        metrics.request_count = 10
        metrics.cache_hits = 7
        metrics.cache_misses = 3
        metrics.total_response_time = 5.0
        metrics.min_response_time = 0.1
        metrics.max_response_time = 1.0
        
        result = metrics.to_dict()
        
        assert result['request_count'] == 10
        assert result['cache_hit_rate'] == 70.0
        assert result['avg_response_time_ms'] == 500.0
        assert result['min_response_time_ms'] == 100.0
        assert result['max_response_time_ms'] == 1000.0


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])



class TestMCPParallelization:
    """Test MCP query parallelization"""
    
    @pytest.mark.asyncio
    async def test_parallel_mcp_queries(self):
        """Test parallel execution of MCP queries"""
        service = PerformanceService(enable_metrics=True)
        
        mcp_queries = [
            {'mcp_name': 'aws-docs', 'query': 'Lambda pricing', 'params': {}},
            {'mcp_name': 'well-architected', 'query': 'Security', 'params': {}},
            {'mcp_name': 'github-analysis', 'query': 'Agent patterns', 'params': {}}
        ]
        
        start_time = time.time()
        results = await service.parallel_mcp_queries(
            mcp_queries,
            max_concurrent=3,
            cache_results=True
        )
        elapsed = time.time() - start_time
        
        # Should complete quickly (parallel)
        assert elapsed < 1.0
        
        # Should return results for all queries
        assert len(results) == 3
        
        # Check result structure
        for result in results:
            assert 'mcp_name' in result
            assert 'result' in result or 'error' in result
    
    @pytest.mark.asyncio
    async def test_parallel_mcp_queries_with_caching(self):
        """Test MCP query caching"""
        service = PerformanceService(enable_metrics=True)
        
        mcp_queries = [
            {'mcp_name': 'aws-docs', 'query': 'Lambda', 'params': {}}
        ]
        
        # First call - cache miss
        results1 = await service.parallel_mcp_queries(
            mcp_queries,
            cache_results=True,
            cache_ttl=60
        )
        
        # Second call - should be cached
        results2 = await service.parallel_mcp_queries(
            mcp_queries,
            cache_results=True,
            cache_ttl=60
        )
        
        # Both should return results
        assert len(results1) == 1
        assert len(results2) == 1
        
        # Second call should be from cache
        assert results2[0].get('cached') == True
    
    @pytest.mark.asyncio
    async def test_parallel_execute_with_timeout(self):
        """Test parallel execution with timeout"""
        service = PerformanceService(enable_metrics=True)
        
        async def slow_task():
            await asyncio.sleep(2.0)
            return "completed"
        
        async def fast_task():
            await asyncio.sleep(0.1)
            return "completed"
        
        tasks = [
            lambda: slow_task(),
            lambda: fast_task(),
            lambda: fast_task()
        ]
        
        # Execute with 1 second timeout
        results = await service.parallel_execute(
            tasks,
            max_concurrent=3,
            timeout_seconds=1.0
        )
        
        # Slow task should timeout (return None)
        assert results[0] is None
        
        # Fast tasks should complete
        assert results[1] == "completed"
        assert results[2] == "completed"


class TestResponseStreaming:
    """Test response streaming functionality"""
    
    @pytest.mark.asyncio
    async def test_stream_chunks(self):
        """Test streaming in chunks mode"""
        service = PerformanceService(enable_metrics=True)
        
        async def generate_chunks():
            for i in range(5):
                yield f"chunk_{i}"
                await asyncio.sleep(0.01)
        
        chunks = []
        async for chunk in service.stream_response(
            generate_chunks(),
            mode=StreamingMode.CHUNKS
        ):
            chunks.append(chunk)
        
        assert len(chunks) == 5
        assert chunks[0] == "chunk_0"
        assert chunks[4] == "chunk_4"
        assert service.metrics.streaming_requests == 1
    
    @pytest.mark.asyncio
    async def test_stream_lines(self):
        """Test streaming in lines mode"""
        service = PerformanceService(enable_metrics=True)
        
        async def generate_lines():
            yield "line 1\n"
            yield "line 2\n"
            yield "line 3"
        
        lines = []
        async for line in service.stream_response(
            generate_lines(),
            mode=StreamingMode.LINES
        ):
            lines.append(line)
        
        # Should receive complete lines
        assert len(lines) >= 2
    
    @pytest.mark.asyncio
    async def test_stream_with_cache(self):
        """Test streaming while caching result"""
        service = PerformanceService(enable_metrics=True)
        
        async def generate_data():
            for i in range(3):
                yield f"data_{i}"
        
        # Stream and cache
        chunks = []
        async for chunk in service.stream_with_cache(
            generate_data(),
            cache_key="test_stream",
            ttl_seconds=60
        ):
            chunks.append(chunk)
        
        assert len(chunks) == 3
        
        # Check if cached (would need to verify cache contains the data)
        # This is a basic test - in production, verify cache content


class TestCacheWarmup:
    """Test cache warmup functionality"""
    
    @pytest.mark.asyncio
    async def test_warmup_cache(self):
        """Test cache warmup with common queries"""
        service = PerformanceService(enable_metrics=True)
        
        call_count = 0
        
        async def expensive_func(x: int) -> int:
            nonlocal call_count
            call_count += 1
            await asyncio.sleep(0.1)
            return x * 2
        
        warmup_queries = [
            {
                'func': expensive_func,
                'cache_key': 'expensive',
                'ttl': 300,
                'args': [5],
                'kwargs': {}
            },
            {
                'func': expensive_func,
                'cache_key': 'expensive',
                'ttl': 300,
                'args': [10],
                'kwargs': {}
            }
        ]
        
        # Warmup cache
        await service.warmup_cache(warmup_queries)
        
        # Functions should have been called
        assert call_count == 2
        
        # Subsequent calls should be cached
        result1 = await service.cached_call(expensive_func, 'expensive', 300, 5)
        result2 = await service.cached_call(expensive_func, 'expensive', 300, 10)
        
        # Should not call function again (cached)
        assert call_count == 2
        assert result1 == 10
        assert result2 == 20


class TestHybridCaching:
    """Test hybrid caching strategy"""
    
    @pytest.mark.asyncio
    async def test_hybrid_cache_strategy(self):
        """Test hybrid caching with memory and ElastiCache"""
        # Note: This test will use in-memory fallback if ElastiCache not available
        service = PerformanceService(
            cache_strategy=CacheStrategy.HYBRID,
            enable_metrics=True
        )
        
        async def test_func(x: int) -> int:
            return x * 2
        
        # First call - cache miss
        result1 = await service.cached_call(test_func, 'test', 60, 5)
        assert result1 == 10
        assert service.metrics.cache_misses == 1
        
        # Second call - cache hit
        result2 = await service.cached_call(test_func, 'test', 60, 5)
        assert result2 == 10
        assert service.metrics.cache_hits == 1
    
    @pytest.mark.asyncio
    async def test_cache_strategy_metrics(self):
        """Test metrics include cache strategy info"""
        service = PerformanceService(
            cache_strategy=CacheStrategy.HYBRID,
            enable_metrics=True
        )
        
        metrics = service.get_metrics()
        
        assert 'cache_strategy' in metrics
        assert metrics['cache_strategy'] == 'hybrid'
        assert 'cache' in metrics
        assert 'performance' in metrics


class TestPerformanceOptimization:
    """Test overall performance optimization"""
    
    @pytest.mark.asyncio
    async def test_response_time_target(self):
        """Test that cached responses meet <100ms target"""
        service = PerformanceService(enable_metrics=True)
        
        async def fast_func() -> str:
            return "result"
        
        # First call to cache
        await service.cached_call(fast_func, 'fast', 300)
        
        # Measure cached call
        start = time.time()
        result = await service.cached_call(fast_func, 'fast', 300)
        elapsed = time.time() - start
        
        # Should be very fast (<100ms)
        assert elapsed < 0.1
        assert result == "result"
    
    @pytest.mark.asyncio
    async def test_parallel_speedup(self):
        """Test that parallel execution is faster than sequential"""
        service = PerformanceService(enable_metrics=True)
        
        async def task():
            await asyncio.sleep(0.1)
            return "done"
        
        # Sequential execution
        start_seq = time.time()
        for _ in range(5):
            await task()
        seq_time = time.time() - start_seq
        
        # Parallel execution
        tasks = [lambda: task() for _ in range(5)]
        start_par = time.time()
        await service.parallel_execute(tasks, max_concurrent=5)
        par_time = time.time() - start_par
        
        # Parallel should be significantly faster
        assert par_time < seq_time / 2
    
    @pytest.mark.asyncio
    async def test_comprehensive_metrics(self):
        """Test comprehensive metrics collection"""
        service = PerformanceService(enable_metrics=True)
        
        async def test_func(x: int) -> int:
            await asyncio.sleep(0.01)
            return x * 2
        
        # Execute various operations
        await service.cached_call(test_func, 'test', 60, 1)  # Miss
        await service.cached_call(test_func, 'test', 60, 1)  # Hit
        await service.cached_call(test_func, 'test', 60, 2)  # Miss
        
        tasks = [lambda: test_func(i) for i in range(3)]
        await service.parallel_execute(tasks)
        
        # Get metrics
        metrics = service.get_metrics()
        
        # Verify all metrics are present
        assert 'performance' in metrics
        perf = metrics['performance']
        
        assert perf['request_count'] >= 3
        assert perf['cache_hits'] >= 1
        assert perf['cache_misses'] >= 2
        assert perf['cache_hit_rate'] > 0
        assert perf['avg_response_time_ms'] > 0
        assert perf['parallel_requests'] >= 3
        
        # Verify cache stats
        assert 'cache' in metrics


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
