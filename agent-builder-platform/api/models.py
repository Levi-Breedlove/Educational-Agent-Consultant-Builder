#!/usr/bin/env python3
"""
Pydantic Models for Request/Response Validation
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

# Enums
class ExperienceLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class WorkflowPhase(str, Enum):
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"

class SessionStatus(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

# Request Models
class CreateSessionRequest(BaseModel):
    user_id: Optional[str] = Field(None, description="User identifier")
    experience_level: ExperienceLevel = Field(ExperienceLevel.BEGINNER, description="User experience level")
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "user-123",
                "experience_level": "beginner"
            }
        }

class RequirementsRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    user_input: str = Field(..., min_length=10, max_length=5000, description="User requirements description")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "user_input": "Build a chatbot that answers customer questions using AI",
                "context": {
                    "budget_range": "low",
                    "timeline": "2_weeks"
                }
            }
        }

class FeedbackRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    feedback_type: str = Field(..., description="Type of feedback")
    content: str = Field(..., description="Feedback content")
    rating: Optional[int] = Field(None, ge=1, le=5, description="Rating 1-5")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "feedback_type": "clarification",
                "content": "I need more details about cost",
                "rating": 4
            }
        }

# Response Models
class SessionResponse(BaseModel):
    session_id: str
    status: SessionStatus
    current_phase: WorkflowPhase
    created_at: str
    updated_at: str
    experience_level: ExperienceLevel
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "status": "active",
                "current_phase": "requirements",
                "created_at": "2025-10-03T10:00:00Z",
                "updated_at": "2025-10-03T10:05:00Z",
                "experience_level": "beginner"
            }
        }

class RequirementsResponse(BaseModel):
    session_id: str
    use_case_analysis: Dict[str, Any]
    service_recommendations: List[Dict[str, Any]]
    cost_analysis: Dict[str, Any]
    security_analysis: Dict[str, Any]
    clarifying_questions: List[str]
    confidence_score: float = Field(..., ge=0.0, le=1.0)
    next_steps: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "use_case_analysis": {
                    "primary_use_case": "chatbot",
                    "complexity": "medium"
                },
                "service_recommendations": [
                    {
                        "service_name": "AWS Lambda",
                        "reasoning": "Serverless compute for chatbot logic"
                    }
                ],
                "cost_analysis": {
                    "estimated_monthly_cost": "$15-30"
                },
                "security_analysis": {
                    "recommendations": ["Enable encryption", "Use IAM roles"]
                },
                "clarifying_questions": [
                    "What is the expected number of users?"
                ],
                "confidence_score": 0.97,
                "next_steps": [
                    "Answer clarifying questions",
                    "Proceed to architecture design"
                ]
            }
        }

class StatusResponse(BaseModel):
    session_id: str
    status: SessionStatus
    current_phase: WorkflowPhase
    progress_percentage: int = Field(..., ge=0, le=100)
    estimated_time_remaining: Optional[int] = None  # seconds
    last_activity: str
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "status": "active",
                "current_phase": "architecture",
                "progress_percentage": 45,
                "estimated_time_remaining": 1200,
                "last_activity": "2025-10-03T10:15:00Z"
            }
        }

class RecommendationsResponse(BaseModel):
    session_id: str
    recommendations: List[Dict[str, Any]]
    confidence_score: float
    reasoning: str
    alternatives: Optional[List[Dict[str, Any]]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "recommendations": [
                    {
                        "type": "service",
                        "name": "AWS Lambda",
                        "priority": "high"
                    }
                ],
                "confidence_score": 0.96,
                "reasoning": "Based on your requirements...",
                "alternatives": []
            }
        }
