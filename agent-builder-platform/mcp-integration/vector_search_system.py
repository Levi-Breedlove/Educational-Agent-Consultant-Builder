#!/usr/bin/env python3
"""
Agent Builder Platform - Vector Search System
Amazon Bedrock Titan integration with semantic search capabilities
"""

import json
import logging
import asyncio
import numpy as np
from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import time
import hashlib
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SearchStrategy(Enum):
    """Search strategy options"""
    VECTOR_PRIMARY = "vector_primary"
    TEXT_FALLBACK = "text_fallback"
    HYBRID = "hybrid"

class EmbeddingModel(Enum):
    """Supported embedding models"""
    TITAN_EMBED_TEXT_V1 = "amazon.titan-embed-text-v1"

@dataclass
class VectorSearchConfig:
    """Configuration for vector search system"""
    embedding_model: EmbeddingModel = EmbeddingModel.TITAN_EMBED_TEXT_V1
    embedding_dimensions: int = 1536
    similarity_threshold: float = 0.7
    max_results: int = 10
    batch_size: int = 25
    cache_ttl_hours: int = 24
    cost_optimization: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'embedding_model': self.embedding_model.value,
            'embedding_dimensions': self.embedding_dimensions,
            'similarity_threshold': self.similarity_threshold,
            'max_results': self.max_results,
            'batch_size': self.batch_size,
            'cache_ttl_hours': self.cache_ttl_hours,
            'cost_optimization': self.cost_optimization
        }

@dataclass
class VectorSearchResult:
    """Result from vector search"""
    content_id: str
    content: str
    title: str
    source: str
    similarity_score: float
    relevance_score: float
    search_method: str
    confidence: float
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class MockBedrockClient:
    """Mock Bedrock client for development (no actual AWS calls)"""
    
    def __init__(self, config: VectorSearchConfig):
        self.config = config
        logger.info(f"Mock Bedrock client initialized with model: {config.embedding_model.value}")
    
    async def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate mock embeddings (in production, this would call Bedrock)"""
        embeddings = []
        
        for text in texts:
            # Generate deterministic mock embeddings based on text hash
            text_hash = hashlib.md5(text.encode()).hexdigest()
            
            # Create a pseudo-random but deterministic embedding
            np.random.seed(int(text_hash[:8], 16))
            embedding = np.random.normal(0, 1, self.config.embedding_dimensions).tolist()
            
            # Normalize the embedding
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = (np.array(embedding) / norm).tolist()
            
            embeddings.append(embedding)
        
        logger.info(f"Generated {len(embeddings)} mock embeddings")
        return embeddings
    
    async def generate_single_embedding(self, text: str) -> List[float]:
        """Generate a single embedding"""
        embeddings = await self.generate_embeddings([text])
        return embeddings[0]

class VectorStorage:
    """Vector storage system using DynamoDB schema"""
    
    def __init__(self, config: VectorSearchConfig):
        self.config = config
        self.vectors: Dict[str, Dict[str, Any]] = {}  # Mock storage
        logger.info("Vector storage initialized (mock mode)")
    
    async def store_vector(self, content_id: str, content: str, title: str, 
                          source: str, embedding: List[float], metadata: Dict[str, Any] = None):
        """Store a vector with its content"""
        vector_data = {
            'content_id': content_id,
            'content': content,
            'title': title,
            'source': source,
            'embedding': embedding,
            'metadata': metadata or {},
            'created_at': datetime.now().isoformat(),
            'embedding_model': self.config.embedding_model.value
        }
        
        self.vectors[content_id] = vector_data
        logger.debug(f"Stored vector for content: {content_id}")
    
    async def search_similar_vectors(self, query_embedding: List[float], 
                                   max_results: int = None) -> List[Dict[str, Any]]:
        """Search for similar vectors using cosine similarity"""
        if not self.vectors:
            return []
        
        max_results = max_results or self.config.max_results
        similarities = []
        
        query_array = np.array(query_embedding)
        
        for content_id, vector_data in self.vectors.items():
            stored_embedding = np.array(vector_data['embedding'])
            
            # Calculate cosine similarity
            similarity = np.dot(query_array, stored_embedding) / (
                np.linalg.norm(query_array) * np.linalg.norm(stored_embedding)
            )
            
            if similarity >= self.config.similarity_threshold:
                similarities.append({
                    'content_id': content_id,
                    'similarity_score': float(similarity),
                    'vector_data': vector_data
                })
        
        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similarities[:max_results]

class VectorSearchSystem:
    """
    Comprehensive vector search system with Amazon Bedrock integration
    """
    
    def __init__(self, config: VectorSearchConfig = None):
        self.config = config or VectorSearchConfig()
        self.bedrock_client = MockBedrockClient(self.config)
        self.vector_storage = VectorStorage(self.config)
        self.embedding_cache: Dict[str, Tuple[List[float], datetime]] = {}
        self.initialized = False
        
        logger.info("Vector Search System initializing...")
    
    async def initialize(self) -> bool:
        """Initialize the vector search system"""
        try:
            logger.info("Initializing vector search system...")
            
            # Initialize sample data for testing
            await self._initialize_sample_data()
            
            self.initialized = True
            logger.info(" Vector Search System initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f" Failed to initialize vector search system: {e}")
            return False
    
    async def _initialize_sample_data(self):
        """Initialize with sample data for testing"""
        sample_content = [
            {
                'content_id': 'aws-lambda-1',
                'title': 'AWS Lambda Best Practices',
                'content': 'AWS Lambda is a serverless compute service that runs code in response to events. Best practices include optimizing memory allocation, using environment variables, and implementing proper error handling.',
                'source': 'aws_documentation',
                'metadata': {'category': 'serverless', 'service': 'lambda'}
            },
            {
                'content_id': 'chatbot-patterns-1',
                'title': 'Chatbot Architecture Patterns',
                'content': 'Modern chatbots require scalable architecture with natural language processing, intent recognition, and integration with backend systems. Consider using API Gateway, Lambda, and DynamoDB for serverless chatbot solutions.',
                'source': 'agent_patterns',
                'metadata': {'category': 'chatbot', 'pattern': 'serverless'}
            },
            {
                'content_id': 'cost-optimization-1',
                'title': 'AWS Cost Optimization Strategies',
                'content': 'Effective cost optimization involves right-sizing instances, using reserved instances, implementing auto-scaling, and monitoring usage patterns. Consider AWS Cost Explorer and Trusted Advisor for insights.',
                'source': 'aws_pricing',
                'metadata': {'category': 'cost', 'service': 'general'}
            }
        ]
        
        for item in sample_content:
            embedding = await self.bedrock_client.generate_single_embedding(item['content'])
            await self.vector_storage.store_vector(
                item['content_id'],
                item['content'],
                item['title'],
                item['source'],
                embedding,
                item['metadata']
            )
        
        logger.info(f"Initialized with {len(sample_content)} sample vectors")
    
    async def generate_query_embedding(self, query: str) -> List[float]:
        """Generate embedding for a query with caching"""
        # Check cache first
        cache_key = hashlib.md5(query.encode()).hexdigest()
        
        if cache_key in self.embedding_cache:
            cached_embedding, cached_time = self.embedding_cache[cache_key]
            if datetime.now() - cached_time < timedelta(hours=self.config.cache_ttl_hours):
                logger.debug("Using cached query embedding")
                return cached_embedding
        
        # Generate new embedding
        embedding = await self.bedrock_client.generate_single_embedding(query)
        
        # Cache the result
        self.embedding_cache[cache_key] = (embedding, datetime.now())
        
        return embedding
    
    async def semantic_search(self, query: str, search_strategy: SearchStrategy = SearchStrategy.VECTOR_PRIMARY,
                            max_results: int = None) -> List[VectorSearchResult]:
        """Perform semantic search with intelligent strategy routing"""
        if not self.initialized:
            raise RuntimeError("Vector search system not initialized")
        
        max_results = max_results or self.config.max_results
        
        try:
            if search_strategy == SearchStrategy.VECTOR_PRIMARY:
                return await self._vector_search(query, max_results)
            elif search_strategy == SearchStrategy.TEXT_FALLBACK:
                return await self._text_search(query, max_results)
            elif search_strategy == SearchStrategy.HYBRID:
                return await self._hybrid_search(query, max_results)
            else:
                raise ValueError(f"Unknown search strategy: {search_strategy}")
                
        except Exception as e:
            logger.error(f"Search failed with strategy {search_strategy}: {e}")
            # Graceful degradation to text search
            if search_strategy != SearchStrategy.TEXT_FALLBACK:
                logger.info("Falling back to text search")
                return await self._text_search(query, max_results)
            raise
    
    async def _vector_search(self, query: str, max_results: int) -> List[VectorSearchResult]:
        """Perform vector similarity search"""
        query_embedding = await self.generate_query_embedding(query)
        similar_vectors = await self.vector_storage.search_similar_vectors(query_embedding, max_results)
        
        results = []
        for item in similar_vectors:
            vector_data = item['vector_data']
            
            result = VectorSearchResult(
                content_id=vector_data['content_id'],
                content=vector_data['content'],
                title=vector_data['title'],
                source=vector_data['source'],
                similarity_score=item['similarity_score'],
                relevance_score=item['similarity_score'],  # For vector search, similarity = relevance
                search_method='vector_primary',
                confidence=self._calculate_confidence(item['similarity_score'], 'vector'),
                metadata=vector_data['metadata']
            )
            results.append(result)
        
        logger.info(f"Vector search returned {len(results)} results")
        return results
    
    async def _text_search(self, query: str, max_results: int) -> List[VectorSearchResult]:
        """Perform text-based search as fallback"""
        query_lower = query.lower()
        results = []
        
        for content_id, vector_data in self.vector_storage.vectors.items():
            content_lower = vector_data['content'].lower()
            title_lower = vector_data['title'].lower()
            
            # Simple text matching score
            content_matches = content_lower.count(query_lower)
            title_matches = title_lower.count(query_lower) * 2  # Weight title matches higher
            
            if content_matches > 0 or title_matches > 0:
                relevance_score = (content_matches + title_matches) / len(query_lower.split())
                
                result = VectorSearchResult(
                    content_id=content_id,
                    content=vector_data['content'],
                    title=vector_data['title'],
                    source=vector_data['source'],
                    similarity_score=0.0,  # No vector similarity in text search
                    relevance_score=min(relevance_score, 1.0),
                    search_method='text_fallback',
                    confidence=self._calculate_confidence(relevance_score, 'text'),
                    metadata=vector_data['metadata']
                )
                results.append(result)
        
        # Sort by relevance score
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        logger.info(f"Text search returned {len(results[:max_results])} results")
        return results[:max_results]
    
    async def _hybrid_search(self, query: str, max_results: int) -> List[VectorSearchResult]:
        """Perform hybrid search combining vector and text methods"""
        # Get results from both methods
        vector_results = await self._vector_search(query, max_results)
        text_results = await self._text_search(query, max_results)
        
        # Combine and deduplicate results
        combined_results = {}
        
        # Add vector results
        for result in vector_results:
            result.search_method = 'hybrid_vector'
            combined_results[result.content_id] = result
        
        # Add text results (if not already present)
        for result in text_results:
            if result.content_id not in combined_results:
                result.search_method = 'hybrid_text'
                combined_results[result.content_id] = result
            else:
                # Boost confidence for items found in both methods
                existing = combined_results[result.content_id]
                existing.confidence = min(existing.confidence * 1.2, 1.0)
                existing.search_method = 'hybrid_both'
        
        # Sort by combined score (similarity + relevance + confidence)
        final_results = list(combined_results.values())
        final_results.sort(key=lambda x: (x.similarity_score + x.relevance_score + x.confidence) / 3, reverse=True)
        
        logger.info(f"Hybrid search returned {len(final_results[:max_results])} results")
        return final_results[:max_results]
    
    def _calculate_confidence(self, score: float, method: str) -> float:
        """Calculate confidence score based on search method and score"""
        base_confidence = {
            'vector': 0.9,
            'text': 0.6,
            'hybrid': 0.8
        }.get(method, 0.5)
        
        # Adjust confidence based on score
        confidence = base_confidence * score
        return min(max(confidence, 0.0), 1.0)
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            'initialized': self.initialized,
            'total_vectors': len(self.vector_storage.vectors),
            'cache_size': len(self.embedding_cache),
            'config': self.config.to_dict(),
            'embedding_model': self.config.embedding_model.value,
            'similarity_threshold': self.config.similarity_threshold
        }

# Test function
async def test_vector_search_system():
    """Test the vector search system"""
    try:
        print(" Testing Vector Search System...")
        
        config = VectorSearchConfig(
            similarity_threshold=0.5,  # Lower threshold for testing
            max_results=5
        )
        
        system = VectorSearchSystem(config)
        
        if await system.initialize():
            print(" Vector Search System initialized successfully")
            
            # Test vector search
            print("\n--- Testing Vector Search ---")
            results = await system.semantic_search(
                "serverless chatbot architecture with AWS Lambda",
                SearchStrategy.VECTOR_PRIMARY
            )
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.title} (similarity: {result.similarity_score:.3f}, confidence: {result.confidence:.3f})")
            
            # Test text search
            print("\n--- Testing Text Search ---")
            results = await system.semantic_search(
                "cost optimization",
                SearchStrategy.TEXT_FALLBACK
            )
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.title} (relevance: {result.relevance_score:.3f}, confidence: {result.confidence:.3f})")
            
            # Test hybrid search
            print("\n--- Testing Hybrid Search ---")
            results = await system.semantic_search(
                "AWS Lambda chatbot",
                SearchStrategy.HYBRID
            )
            
            for i, result in enumerate(results, 1):
                print(f"{i}. {result.title} (method: {result.search_method}, confidence: {result.confidence:.3f})")
            
            # Show system stats
            stats = system.get_system_stats()
            print(f"\n System Stats:")
            print(f"   - Total vectors: {stats['total_vectors']}")
            print(f"   - Cache size: {stats['cache_size']}")
            print(f"   - Embedding model: {stats['embedding_model']}")
            
            print("\n Vector Search System test completed successfully!")
            return True
        else:
            print(" Vector Search System initialization failed")
            return False
            
    except Exception as e:
        print(f" Vector Search System test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_vector_search_system())
