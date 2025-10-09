#!/usr/bin/env python3
"""
Rate Limiting and Cost Control Module
Per-user and per-session rate limiting with cost tracking
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Tuple
from fastapi import HTTPException, status, Request
from collections import defaultdict
import logging
import asyncio

logger = logging.getLogger(__name__)

class RateLimitTier:
    """Rate limit tier configuration"""
    
    FREE = {
        "name": "free",
        "requests_per_minute": 10,
        "requests_per_hour": 100,
        "requests_per_day": 500,
        "max_concurrent_sessions": 2,
        "max_agents_per_day": 5,
        "cost_limit_per_day": 5.0  # USD
    }
    
    BASIC = {
        "name": "basic",
        "requests_per_minute": 30,
        "requests_per_hour": 500,
        "requests_per_day": 2000,
        "max_concurrent_sessions": 5,
        "max_agents_per_day": 20,
        "cost_limit_per_day": 20.0
    }
    
    PREMIUM = {
        "name": "premium",
        "requests_per_minute": 100,
        "requests_per_hour": 2000,
        "requests_per_day": 10000,
        "max_concurrent_sessions": 20,
        "max_agents_per_day": 100,
        "cost_limit_per_day": 100.0
    }
    
    @classmethod
    def get_tier(cls, tier_name: str) -> dict:
        """Get tier configuration by name"""
        tiers = {
            "free": cls.FREE,
            "basic": cls.BASIC,
            "premium": cls.PREMIUM
        }
        return tiers.get(tier_name.lower(), cls.FREE)

class RateLimiter:
    """Rate limiter with sliding window algorithm"""
    
    def __init__(self):
        # Request tracking: {user_id: [(timestamp, endpoint), ...]}
        self.request_history: Dict[str, list] = defaultdict(list)
        
        # Session tracking: {user_id: [session_id, ...]}
        self.active_sessions: Dict[str, list] = defaultdict(list)
        
        # Agent creation tracking: {user_id: [(timestamp, agent_id), ...]}
        self.agent_creation_history: Dict[str, list] = defaultdict(list)
        
        # Cost tracking: {user_id: [(timestamp, cost), ...]}
        self.cost_history: Dict[str, list] = defaultdict(list)
        
        # Cleanup task
        self._cleanup_task = None
    
    async def start_cleanup_task(self):
        """Start background cleanup task"""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_old_data())
    
    async def _cleanup_old_data(self):
        """Periodically cleanup old tracking data"""
        while True:
            try:
                await asyncio.sleep(300)  # Every 5 minutes
                
                now = datetime.now(timezone.utc)
                cutoff = now - timedelta(days=1)
                
                # Cleanup request history
                for user_id in list(self.request_history.keys()):
                    self.request_history[user_id] = [
                        (ts, endpoint) for ts, endpoint in self.request_history[user_id]
                        if ts > cutoff
                    ]
                    if not self.request_history[user_id]:
                        del self.request_history[user_id]
                
                # Cleanup agent creation history
                for user_id in list(self.agent_creation_history.keys()):
                    self.agent_creation_history[user_id] = [
                        (ts, agent_id) for ts, agent_id in self.agent_creation_history[user_id]
                        if ts > cutoff
                    ]
                    if not self.agent_creation_history[user_id]:
                        del self.agent_creation_history[user_id]
                
                # Cleanup cost history
                for user_id in list(self.cost_history.keys()):
                    self.cost_history[user_id] = [
                        (ts, cost) for ts, cost in self.cost_history[user_id]
                        if ts > cutoff
                    ]
                    if not self.cost_history[user_id]:
                        del self.cost_history[user_id]
                
                logger.info("Rate limiter cleanup completed")
                
            except Exception as e:
                logger.error(f"Cleanup task error: {e}")
    
    def _count_requests_in_window(
        self, 
        user_id: str, 
        window_seconds: int
    ) -> int:
        """Count requests in time window"""
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(seconds=window_seconds)
        
        return sum(
            1 for ts, _ in self.request_history[user_id]
            if ts > cutoff
        )
    
    def check_rate_limit(
        self, 
        user_id: str, 
        tier_name: str,
        endpoint: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if request is within rate limits
        
        Args:
            user_id: User identifier
            tier_name: Rate limit tier
            endpoint: API endpoint
            
        Returns:
            Tuple of (allowed, error_message)
        """
        tier = RateLimitTier.get_tier(tier_name)
        
        # Check per-minute limit
        requests_per_minute = self._count_requests_in_window(user_id, 60)
        if requests_per_minute >= tier["requests_per_minute"]:
            return False, f"Rate limit exceeded: {tier['requests_per_minute']} requests per minute"
        
        # Check per-hour limit
        requests_per_hour = self._count_requests_in_window(user_id, 3600)
        if requests_per_hour >= tier["requests_per_hour"]:
            return False, f"Rate limit exceeded: {tier['requests_per_hour']} requests per hour"
        
        # Check per-day limit
        requests_per_day = self._count_requests_in_window(user_id, 86400)
        if requests_per_day >= tier["requests_per_day"]:
            return False, f"Rate limit exceeded: {tier['requests_per_day']} requests per day"
        
        return True, None
    
    def record_request(self, user_id: str, endpoint: str):
        """Record a request"""
        now = datetime.now(timezone.utc)
        self.request_history[user_id].append((now, endpoint))
    
    def check_session_limit(
        self, 
        user_id: str, 
        tier_name: str
    ) -> Tuple[bool, Optional[str]]:
        """Check if user can create new session"""
        tier = RateLimitTier.get_tier(tier_name)
        
        active_count = len(self.active_sessions[user_id])
        if active_count >= tier["max_concurrent_sessions"]:
            return False, f"Maximum concurrent sessions exceeded: {tier['max_concurrent_sessions']}"
        
        return True, None
    
    def add_session(self, user_id: str, session_id: str):
        """Add active session"""
        if session_id not in self.active_sessions[user_id]:
            self.active_sessions[user_id].append(session_id)
    
    def remove_session(self, user_id: str, session_id: str):
        """Remove active session"""
        if session_id in self.active_sessions[user_id]:
            self.active_sessions[user_id].remove(session_id)
    
    def check_agent_creation_limit(
        self, 
        user_id: str, 
        tier_name: str
    ) -> Tuple[bool, Optional[str]]:
        """Check if user can create new agent"""
        tier = RateLimitTier.get_tier(tier_name)
        
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=1)
        
        agents_today = sum(
            1 for ts, _ in self.agent_creation_history[user_id]
            if ts > cutoff
        )
        
        if agents_today >= tier["max_agents_per_day"]:
            return False, f"Maximum agents per day exceeded: {tier['max_agents_per_day']}"
        
        return True, None
    
    def record_agent_creation(self, user_id: str, agent_id: str):
        """Record agent creation"""
        now = datetime.now(timezone.utc)
        self.agent_creation_history[user_id].append((now, agent_id))
    
    def check_cost_limit(
        self, 
        user_id: str, 
        tier_name: str,
        additional_cost: float = 0.0
    ) -> Tuple[bool, Optional[str]]:
        """Check if cost is within limits"""
        tier = RateLimitTier.get_tier(tier_name)
        
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(days=1)
        
        cost_today = sum(
            cost for ts, cost in self.cost_history[user_id]
            if ts > cutoff
        )
        
        if cost_today + additional_cost > tier["cost_limit_per_day"]:
            return False, f"Daily cost limit exceeded: ${tier['cost_limit_per_day']:.2f}"
        
        return True, None
    
    def record_cost(self, user_id: str, cost: float):
        """Record cost"""
        now = datetime.now(timezone.utc)
        self.cost_history[user_id].append((now, cost))
    
    def get_usage_stats(self, user_id: str, tier_name: str) -> dict:
        """Get usage statistics for user"""
        tier = RateLimitTier.get_tier(tier_name)
        
        now = datetime.now(timezone.utc)
        
        # Calculate usage
        requests_per_minute = self._count_requests_in_window(user_id, 60)
        requests_per_hour = self._count_requests_in_window(user_id, 3600)
        requests_per_day = self._count_requests_in_window(user_id, 86400)
        
        # Agent creation count
        cutoff_day = now - timedelta(days=1)
        agents_today = sum(
            1 for ts, _ in self.agent_creation_history[user_id]
            if ts > cutoff_day
        )
        
        # Cost today
        cost_today = sum(
            cost for ts, cost in self.cost_history[user_id]
            if ts > cutoff_day
        )
        
        return {
            "tier": tier_name,
            "requests": {
                "per_minute": {
                    "used": requests_per_minute,
                    "limit": tier["requests_per_minute"],
                    "remaining": max(0, tier["requests_per_minute"] - requests_per_minute)
                },
                "per_hour": {
                    "used": requests_per_hour,
                    "limit": tier["requests_per_hour"],
                    "remaining": max(0, tier["requests_per_hour"] - requests_per_hour)
                },
                "per_day": {
                    "used": requests_per_day,
                    "limit": tier["requests_per_day"],
                    "remaining": max(0, tier["requests_per_day"] - requests_per_day)
                }
            },
            "sessions": {
                "active": len(self.active_sessions[user_id]),
                "limit": tier["max_concurrent_sessions"],
                "remaining": max(0, tier["max_concurrent_sessions"] - len(self.active_sessions[user_id]))
            },
            "agents": {
                "created_today": agents_today,
                "limit": tier["max_agents_per_day"],
                "remaining": max(0, tier["max_agents_per_day"] - agents_today)
            },
            "cost": {
                "today": round(cost_today, 2),
                "limit": tier["cost_limit_per_day"],
                "remaining": round(max(0, tier["cost_limit_per_day"] - cost_today), 2)
            }
        }

# Global rate limiter instance
_rate_limiter: Optional[RateLimiter] = None

def get_rate_limiter() -> RateLimiter:
    """Get rate limiter instance"""
    global _rate_limiter
    if _rate_limiter is None:
        _rate_limiter = RateLimiter()
    return _rate_limiter

# Rate limit dependency
async def check_rate_limit(
    request: Request,
    user_id: str,
    tier_name: str = "free",
    rate_limiter: RateLimiter = None
):
    """
    Dependency to check rate limits
    
    Args:
        request: FastAPI request
        user_id: User identifier
        tier_name: Rate limit tier
        rate_limiter: Rate limiter instance
        
    Raises:
        HTTPException: If rate limit exceeded
    """
    if rate_limiter is None:
        rate_limiter = get_rate_limiter()
    
    endpoint = request.url.path
    
    # Check rate limit
    allowed, error_message = rate_limiter.check_rate_limit(user_id, tier_name, endpoint)
    
    if not allowed:
        logger.warning(f"Rate limit exceeded for user {user_id}: {error_message}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=error_message,
            headers={"Retry-After": "60"}
        )
    
    # Record request
    rate_limiter.record_request(user_id, endpoint)
