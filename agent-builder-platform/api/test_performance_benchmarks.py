#!/usr/bin/env python3
"""
Performance Benchmark Tests
Tests API performance, response times, and throughput
"""

import sys
import os
import time
import statistics
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from api.main import app

# Create test client
client = TestClient(app)


class PerformanceBenchmark:
    """Performance benchmark utilities"""
    
    @staticmethod
    def measure_response_time(func, iterations=10):
        """Measure average response time for a function"""
        times = []
        for _ in range(iterations):
            start = time.time()
            func()
            end = time.time()
            times.append((end - start) * 1000)  # Convert to milliseconds
        
        return {
            'min': min(times),
            'max': max(times),
            'avg': statistics.mean(times),
            'median': statistics.median(times),
            'stdev': statistics.stdev(times) if len(times) > 1 else 0
        }
    
    @staticmethod
    def format_time(ms):
        """Format time in milliseconds"""
        return f"{ms:.2f}ms"


class TestResponseTimes:
    """Test response time benchmarks"""
    
    def test_health_check_response_time(self):
        """Benchmark health check endpoint"""
        print("\n  Testing health check response time...")
        
        def health_check():
            response = client.get("/health")
            assert response.status_code == 200
        
        results = PerformanceBenchmark.measure_response_time(health_check, iterations=20)
        
        print(f"    Min: {PerformanceBenchmark.format_time(results['min'])}")
        print(f"    Max: {PerformanceBenchmark.format_time(results['max'])}")
        print(f"    Avg: {PerformanceBenchmark.format_time(results['avg'])}")
        print(f"    Median: {PerformanceBenchmark.format_time(results['median'])}")
        
        # Assert performance targets
        assert results['avg'] < 100, f"Average response time {results['avg']:.2f}ms exceeds 100ms target"
        assert results['median'] < 100, f"Median response time {results['median']:.2f}ms exceeds 100ms target"
    
    def test_session_creation_response_time(self):
        """Benchmark session creation endpoint"""
        print("\n  Testing session creation response time...")
        
        def create_session():
            response = client.post("/api/sessions", json={})
            assert response.status_code == 201
        
        results = PerformanceBenchmark.measure_response_time(create_session, iterations=10)
        
        print(f"    Min: {PerformanceBenchmark.format_time(results['min'])}")
        print(f"    Max: {PerformanceBenchmark.format_time(results['max'])}")
        print(f"    Avg: {PerformanceBenchmark.format_time(results['avg'])}")
        print(f"    Median: {PerformanceBenchmark.format_time(results['median'])}")
        
        # Assert performance targets (more lenient for DB operations)
        assert results['avg'] < 500, f"Average response time {results['avg']:.2f}ms exceeds 500ms target"
    
    def test_session_retrieval_response_time(self):
        """Benchmark session retrieval endpoint"""
        print("\n  Testing session retrieval response time...")
        
        # Create a session first
        create_response = client.post("/api/sessions", json={})
        session_id = create_response.json()["session_id"]
        
        def get_session():
            response = client.get(f"/api/sessions/{session_id}")
            assert response.status_code == 200
        
        results = PerformanceBenchmark.measure_response_time(get_session, iterations=20)
        
        print(f"    Min: {PerformanceBenchmark.format_time(results['min'])}")
        print(f"    Max: {PerformanceBenchmark.format_time(results['max'])}")
        print(f"    Avg: {PerformanceBenchmark.format_time(results['avg'])}")
        print(f"    Median: {PerformanceBenchmark.format_time(results['median'])}")
        
        # Assert performance targets
        assert results['avg'] < 300, f"Average response time {results['avg']:.2f}ms exceeds 300ms target"
    
    def test_metrics_endpoint_response_time(self):
        """Benchmark metrics endpoint"""
        print("\n  Testing metrics endpoint response time...")
        
        def get_metrics():
            response = client.get("/api/metrics")
            assert response.status_code == 200
        
        results = PerformanceBenchmark.measure_response_time(get_metrics, iterations=20)
        
        print(f"    Min: {PerformanceBenchmark.format_time(results['min'])}")
        print(f"    Max: {PerformanceBenchmark.format_time(results['max'])}")
        print(f"    Avg: {PerformanceBenchmark.format_time(results['avg'])}")
        print(f"    Median: {PerformanceBenchmark.format_time(results['median'])}")
        
        # Assert performance targets
        assert results['avg'] < 100, f"Average response time {results['avg']:.2f}ms exceeds 100ms target"


class TestThroughput:
    """Test API throughput"""
    
    def test_concurrent_session_creation(self):
        """Test throughput for concurrent session creation"""
        print("\n  Testing concurrent session creation throughput...")
        
        num_requests = 20
        start_time = time.time()
        
        session_ids = []
        for i in range(num_requests):
            response = client.post("/api/sessions", json={
                "user_id": f"throughput-test-{i}"
            })
            assert response.status_code == 201
            session_ids.append(response.json()["session_id"])
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = num_requests / duration
        
        print(f"    Requests: {num_requests}")
        print(f"    Duration: {duration:.2f}s")
        print(f"    Throughput: {throughput:.2f} req/s")
        
        # Cleanup
        for session_id in session_ids:
            client.delete(f"/api/sessions/{session_id}")
        
        # Assert minimum throughput
        assert throughput > 5, f"Throughput {throughput:.2f} req/s is below 5 req/s minimum"
    
    def test_read_throughput(self):
        """Test throughput for read operations"""
        print("\n  Testing read operation throughput...")
        
        # Create a session
        create_response = client.post("/api/sessions", json={})
        session_id = create_response.json()["session_id"]
        
        num_requests = 50
        start_time = time.time()
        
        for _ in range(num_requests):
            response = client.get(f"/api/sessions/{session_id}")
            assert response.status_code == 200
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = num_requests / duration
        
        print(f"    Requests: {num_requests}")
        print(f"    Duration: {duration:.2f}s")
        print(f"    Throughput: {throughput:.2f} req/s")
        
        # Cleanup
        client.delete(f"/api/sessions/{session_id}")
        
        # Assert minimum throughput (reads should be faster)
        assert throughput > 10, f"Throughput {throughput:.2f} req/s is below 10 req/s minimum"


class TestCachePerformance:
    """Test cache performance improvements"""
    
    def test_cache_hit_performance(self):
        """Test that cache hits are faster than cache misses"""
        print("\n  Testing cache performance...")
        
        # Clear cache first
        client.post("/api/cache/clear")
        
        # First request (cache miss)
        start = time.time()
        response1 = client.get("/api/metrics")
        time1 = (time.time() - start) * 1000
        assert response1.status_code == 200
        
        # Second request (potential cache hit)
        start = time.time()
        response2 = client.get("/api/metrics")
        time2 = (time.time() - start) * 1000
        assert response2.status_code == 200
        
        print(f"    First request (cache miss): {time1:.2f}ms")
        print(f"    Second request: {time2:.2f}ms")
        print(f"    Improvement: {((time1 - time2) / time1 * 100):.1f}%")
        
        # Cache should provide some benefit (or at least not be slower)
        assert time2 <= time1 * 1.5, "Cached request is significantly slower"


class TestScalability:
    """Test API scalability"""
    
    def test_increasing_load(self):
        """Test API behavior under increasing load"""
        print("\n  Testing API under increasing load...")
        
        load_levels = [5, 10, 20]
        results = []
        
        for load in load_levels:
            start_time = time.time()
            
            for i in range(load):
                response = client.get("/health")
                assert response.status_code == 200
            
            duration = time.time() - start_time
            avg_time = (duration / load) * 1000
            results.append(avg_time)
            
            print(f"    Load {load}: {avg_time:.2f}ms avg per request")
        
        # Response time shouldn't degrade significantly with load
        # Allow up to 2x degradation
        assert results[-1] < results[0] * 2, "Response time degrades too much under load"


class TestMemoryEfficiency:
    """Test memory efficiency"""
    
    def test_session_cleanup(self):
        """Test that sessions are properly cleaned up"""
        print("\n  Testing session cleanup...")
        
        # Create multiple sessions
        session_ids = []
        for i in range(10):
            response = client.post("/api/sessions", json={})
            assert response.status_code == 201
            session_ids.append(response.json()["session_id"])
        
        # Delete all sessions
        for session_id in session_ids:
            response = client.delete(f"/api/sessions/{session_id}")
            assert response.status_code == 200
        
        # Verify all are deleted
        for session_id in session_ids:
            response = client.get(f"/api/sessions/{session_id}")
            assert response.status_code == 404
        
        print(f"    Successfully cleaned up {len(session_ids)} sessions")


def run_benchmarks():
    """Run all performance benchmarks"""
    print("=" * 80)
    print("PERFORMANCE BENCHMARK SUITE")
    print("=" * 80)
    print()
    print("Target Performance Metrics:")
    print("  - Health check: < 100ms average")
    print("  - Session creation: < 500ms average")
    print("  - Session retrieval: < 300ms average")
    print("  - Metrics endpoint: < 100ms average")
    print("  - Throughput: > 5 req/s for writes, > 10 req/s for reads")
    print()
    
    test_classes = [
        TestResponseTimes,
        TestThroughput,
        TestCachePerformance,
        TestScalability,
        TestMemoryEfficiency
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n{test_class.__name__}")
        print("-" * 80)
        
        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith("test_")]
        
        for method_name in test_methods:
            total_tests += 1
            try:
                method = getattr(test_instance, method_name)
                method()
                print(f"  ✓ {method_name}")
                passed_tests += 1
            except AssertionError as e:
                print(f"  ✗ {method_name}: {e}")
                failed_tests += 1
            except Exception as e:
                print(f"  ✗ {method_name}: {type(e).__name__}: {e}")
                failed_tests += 1
    
    print()
    print("=" * 80)
    print(f"RESULTS: {passed_tests}/{total_tests} benchmarks passed")
    if failed_tests > 0:
        print(f"FAILED: {failed_tests} benchmarks")
        return 1
    else:
        print("ALL BENCHMARKS PASSED ✓")
        return 0


if __name__ == "__main__":
    exit_code = run_benchmarks()
    sys.exit(exit_code)
