#!/usr/bin/env python3
"""
Agent Builder Platform - FastAPI Backend
Main API application with CORS, authentication, and agent integration
"""

from fastapi import FastAPI, HTTPException, Depends, status, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
import logging
import uuid
import io
from datetime import datetime, timezone

from .models import (
    CreateSessionRequest, SessionResponse, SessionStatus, 
    WorkflowPhase, ExperienceLevel, RequirementsRequest, RequirementsResponse,
    FeedbackRequest, StatusResponse, RecommendationsResponse
)
from .session_service import get_session_service, SessionService
from .workflow_service import get_workflow_service, WorkflowService
from .testing_service import get_testing_service, TestingService
from .export_service import get_export_service, ExportService, ExportFormat, DeploymentTarget
from .websocket_service import get_websocket_manager, WebSocketManager
from .performance_service import get_performance_service, PerformanceService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Agent Builder Platform API",
    description="Expert AI consultation system for building production-ready agents",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Performance monitoring middleware
@app.middleware("http")
async def performance_monitoring_middleware(request, call_next):
    """Track performance metrics for all requests"""
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Track response time
        response_time = time.time() - start_time
        
        # Add performance headers
        response.headers["X-Response-Time"] = f"{response_time:.3f}s"
        response.headers["X-Cache-Status"] = "MISS"  # Will be overridden by cached responses
        
        return response
        
    except Exception as e:
        logger.error(f"Request failed: {e}")
        raise

import time

# Pydantic models for request/response validation
class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: str
    agents_available: int

class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    timestamp: str

class DeleteSessionResponse(BaseModel):
    session_id: str
    message: str
    deleted_at: str

class CreateAgentRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    use_case: str = Field(..., min_length=3, max_length=200, description="Use case name")
    description: str = Field(..., min_length=10, max_length=5000, description="Detailed description")
    experience_level: Optional[str] = Field("beginner", description="User experience level")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "use_case": "customer_support_chatbot",
                "description": "Build a chatbot that answers customer questions using AI",
                "experience_level": "beginner"
            }
        }

class CreateAgentResponse(BaseModel):
    agent_id: str
    session_id: str
    status: str
    progress_percentage: float
    created_at: str
    use_case: str
    description: str
    experience_level: str
    vector_search_enabled: bool
    
    class Config:
        schema_extra = {
            "example": {
                "agent_id": "agent-abc123",
                "session_id": "session-abc-123",
                "status": "requirements",
                "progress_percentage": 0.0,
                "created_at": "2025-10-03T10:00:00Z",
                "use_case": "customer_support_chatbot",
                "description": "Build a chatbot...",
                "experience_level": "beginner",
                "vector_search_enabled": True
            }
        }

class FeedbackResponse(BaseModel):
    agent_id: str
    feedback_received: bool
    feedback_type: str
    action: str
    message: str
    next_phase: Optional[str] = None
    timestamp: str
    
    class Config:
        schema_extra = {
            "example": {
                "agent_id": "agent-abc123",
                "feedback_received": True,
                "feedback_type": "approval",
                "action": "phase_approved",
                "message": "Great! Moving to the next phase.",
                "next_phase": "architecture",
                "timestamp": "2025-10-03T10:15:00Z"
            }
        }

class TestExecutionRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    test_types: Optional[List[str]] = Field(None, description="Specific test types to run")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "test_types": ["security", "performance", "cost"]
            }
        }

class TestExecutionResponse(BaseModel):
    agent_id: str
    test_execution_id: str
    timestamp: str
    overall_status: str
    tests_executed: Dict[str, int]
    summary: Dict[str, int]
    production_readiness_score: float
    confidence_score: float
    recommendations: List[str]
    
    class Config:
        schema_extra = {
            "example": {
                "agent_id": "agent-abc123",
                "test_execution_id": "test-xyz789",
                "timestamp": "2025-10-03T10:30:00Z",
                "overall_status": "passed",
                "tests_executed": {
                    "security": 5,
                    "performance": 3,
                    "cost": 2,
                    "integration": 4,
                    "load": 2
                },
                "summary": {
                    "total_tests": 16,
                    "passed": 14,
                    "failed": 1,
                    "warnings": 1
                },
                "production_readiness_score": 0.92,
                "confidence_score": 0.97,
                "recommendations": [
                    "Enable encryption at rest for DynamoDB",
                    "Add CloudWatch alarms for Lambda errors"
                ]
            }
        }

class ValidationReportResponse(BaseModel):
    agent_id: str
    report_id: str
    timestamp: str
    overall_status: str
    production_readiness_score: float
    confidence_score: float
    multi_source_validation: Dict[str, float]
    summary: Dict[str, Any]
    assumptions_detected: List[str]
    recommendations: List[str]
    monitoring: Dict[str, Any]
    details: Optional[Dict[str, Any]] = None
    
    class Config:
        schema_extra = {
            "example": {
                "agent_id": "agent-abc123",
                "report_id": "report-xyz789",
                "timestamp": "2025-10-03T10:30:00Z",
                "overall_status": "passed",
                "production_readiness_score": 0.92,
                "confidence_score": 0.97,
                "multi_source_validation": {
                    "security": 0.98,
                    "performance": 0.96,
                    "cost": 0.95
                },
                "summary": {
                    "security": {"total_findings": 5, "critical": 0, "high": 1},
                    "performance": {"total_metrics": 3, "passed": 2, "failed": 1}
                },
                "assumptions_detected": ["Assumes 1000 concurrent users"],
                "recommendations": ["Enable encryption", "Add monitoring"],
                "monitoring": {"total_configs": 3, "average_completeness": 0.85}
            }
        }

# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
        agents_available=5
    )

# Performance metrics endpoint
@app.get("/api/metrics", tags=["Performance"])
async def get_metrics(
    performance_service: PerformanceService = Depends(get_performance_service)
):
    """
    Get performance metrics
    
    Returns cache statistics, response times, and request counts
    """
    metrics = performance_service.get_metrics()
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "metrics": metrics
    }

# Clear cache endpoint
@app.post("/api/cache/clear", tags=["Performance"])
async def clear_cache(
    performance_service: PerformanceService = Depends(get_performance_service)
):
    """
    Clear all cache entries
    
    Returns confirmation of cache clear
    """
    await performance_service.clear_cache()
    return {
        "message": "Cache cleared successfully",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Reset metrics endpoint
@app.post("/api/metrics/reset", tags=["Performance"])
async def reset_metrics(
    performance_service: PerformanceService = Depends(get_performance_service)
):
    """
    Reset performance metrics
    
    Returns confirmation of metrics reset
    """
    performance_service.reset_metrics()
    return {
        "message": "Metrics reset successfully",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "name": "Agent Builder Platform API",
        "version": "1.0.0",
        "description": "Expert AI consultation system",
        "docs": "/api/docs",
        "health": "/health",
        "metrics": "/api/metrics"
    }

# Session Management Endpoints

@app.post("/api/sessions", response_model=SessionResponse, tags=["Sessions"], status_code=status.HTTP_201_CREATED)
async def create_session(
    request: CreateSessionRequest,
    session_service: SessionService = Depends(get_session_service)
):
    """
    Create a new agent creation session
    
    - **user_id**: Optional user identifier (anonymous if not provided)
    - **experience_level**: User's experience level (beginner, intermediate, advanced, expert)
    
    Returns session details including session_id for subsequent API calls
    """
    try:
        session_data = session_service.create_session(
            user_id=request.user_id,
            experience_level=request.experience_level
        )
        
        return SessionResponse(
            session_id=session_data['session_id'],
            status=SessionStatus(session_data['status']),
            current_phase=WorkflowPhase(session_data['current_phase']),
            created_at=session_data['created_at'],
            updated_at=session_data['updated_at'],
            experience_level=ExperienceLevel(session_data['experience_level'])
        )
    except Exception as e:
        logger.error(f"Error creating session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create session: {str(e)}"
        )


@app.get("/api/sessions/{session_id}", response_model=SessionResponse, tags=["Sessions"])
async def get_session(
    session_id: str,
    session_service: SessionService = Depends(get_session_service)
):
    """
    Retrieve session details by session ID
    
    - **session_id**: Unique session identifier
    
    Returns complete session state including current phase and progress
    """
    try:
        session_data = session_service.get_session(session_id)
        
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}"
            )
        
        return SessionResponse(
            session_id=session_data['session_id'],
            status=SessionStatus(session_data['status']),
            current_phase=WorkflowPhase(session_data['current_phase']),
            created_at=session_data['created_at'],
            updated_at=session_data['updated_at'],
            experience_level=ExperienceLevel(session_data['experience_level'])
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve session: {str(e)}"
        )


@app.delete("/api/sessions/{session_id}", response_model=DeleteSessionResponse, tags=["Sessions"])
async def delete_session(
    session_id: str,
    session_service: SessionService = Depends(get_session_service)
):
    """
    Delete a session and cleanup associated data
    
    - **session_id**: Unique session identifier
    
    Returns confirmation of deletion
    """
    try:
        # Verify session exists before deleting
        session_data = session_service.get_session(session_id)
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}"
            )
        
        # Delete the session
        session_service.delete_session(session_id)
        
        return DeleteSessionResponse(
            session_id=session_id,
            message="Session deleted successfully",
            deleted_at=datetime.now(timezone.utc).isoformat()
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete session: {str(e)}"
        )


# Agent Creation Workflow Endpoints

@app.post("/api/agents/create", response_model=CreateAgentResponse, tags=["Agent Workflow"], status_code=status.HTTP_201_CREATED)
async def create_agent(
    request: CreateAgentRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service),
    session_service: SessionService = Depends(get_session_service)
):
    """
    Start agent creation workflow
    
    - **session_id**: Active session identifier
    - **use_case**: Use case name (e.g., "customer_support_chatbot")
    - **description**: Detailed description of what you want to build
    - **experience_level**: Your experience level (beginner, intermediate, advanced, expert)
    
    Returns agent_id for tracking the workflow
    """
    try:
        # Verify session exists
        session_data = session_service.get_session(request.session_id)
        if not session_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {request.session_id}"
            )
        
        # Create agent workflow
        agent_data = await workflow_service.create_agent_workflow(
            session_id=request.session_id,
            user_id=session_data.get('user_id'),
            use_case=request.use_case,
            description=request.description,
            experience_level=request.experience_level or "beginner"
        )
        
        logger.info(f"Created agent workflow: {agent_data['agent_id']}")
        
        return CreateAgentResponse(**agent_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )


@app.post("/api/agents/{agent_id}/requirements", response_model=RequirementsResponse, tags=["Agent Workflow"])
async def submit_requirements(
    agent_id: str,
    request: RequirementsRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    Submit requirements for agent creation
    
    - **agent_id**: Agent identifier from create_agent
    - **user_input**: Your requirements and needs
    - **context**: Additional context (budget, timeline, etc.)
    
    Returns expert analysis with service recommendations and cost estimates
    """
    try:
        # Submit requirements and get analysis
        result = await workflow_service.submit_requirements(
            agent_id=agent_id,
            user_input=request.user_input,
            context=request.context
        )
        
        analysis = result.get('analysis', {})
        
        # Build response
        response = RequirementsResponse(
            session_id=request.session_id,
            use_case_analysis=analysis.get('use_case_analysis', {}),
            service_recommendations=analysis.get('service_recommendations', []),
            cost_analysis=analysis.get('cost_analysis', {}),
            security_analysis=analysis.get('security_analysis', {}),
            clarifying_questions=analysis.get('clarifying_questions', []),
            confidence_score=analysis.get('confidence_score', 0.0),
            next_steps=analysis.get('next_steps', [])
        )
        
        logger.info(f"Requirements submitted for agent: {agent_id}")
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error submitting requirements: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit requirements: {str(e)}"
        )


@app.post("/api/agents/{agent_id}/feedback", response_model=FeedbackResponse, tags=["Agent Workflow"])
async def process_feedback(
    agent_id: str,
    request: FeedbackRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    Provide feedback during agent creation workflow
    
    - **agent_id**: Agent identifier
    - **feedback_type**: Type of feedback (clarification, approval, modification)
    - **content**: Your feedback content
    - **rating**: Optional rating 1-5
    
    Returns feedback processing result and next actions
    """
    try:
        result = await workflow_service.process_feedback(
            agent_id=agent_id,
            feedback_type=request.feedback_type,
            content=request.content,
            rating=request.rating
        )
        
        logger.info(f"Feedback processed for agent: {agent_id}")
        
        return FeedbackResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error processing feedback: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process feedback: {str(e)}"
        )


@app.get("/api/agents/{agent_id}/status", response_model=StatusResponse, tags=["Agent Workflow"])
async def get_agent_status(
    agent_id: str,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    Get current workflow status
    
    - **agent_id**: Agent identifier
    
    Returns current phase, progress, and activity status
    """
    try:
        status_data = await workflow_service.get_workflow_status(agent_id)
        
        # Calculate estimated time remaining (rough estimate)
        progress = status_data['progress_percentage']
        if progress > 0 and progress < 100:
            # Assume 45 minutes total, calculate remaining
            total_seconds = 45 * 60
            elapsed_ratio = progress / 100
            remaining_seconds = int(total_seconds * (1 - elapsed_ratio))
        else:
            remaining_seconds = None
        
        response = StatusResponse(
            session_id=agent_id,  # Using agent_id as session_id for now
            status=SessionStatus.ACTIVE,
            current_phase=WorkflowPhase(status_data['status']),
            progress_percentage=int(status_data['progress_percentage']),
            estimated_time_remaining=remaining_seconds,
            last_activity=status_data['updated_at']
        )
        
        logger.info(f"Status retrieved for agent: {agent_id}")
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting agent status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get agent status: {str(e)}"
        )


@app.get("/api/agents/{agent_id}/recommendations", response_model=RecommendationsResponse, tags=["Agent Workflow"])
async def get_recommendations(
    agent_id: str,
    recommendation_type: Optional[str] = None,
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    Get AI recommendations for current phase
    
    - **agent_id**: Agent identifier
    - **recommendation_type**: Optional type filter (services, architecture, implementation)
    
    Returns AI-generated recommendations with confidence scores
    """
    try:
        recommendations = await workflow_service.get_recommendations(
            agent_id=agent_id,
            recommendation_type=recommendation_type
        )
        
        logger.info(f"Recommendations retrieved for agent: {agent_id}")
        
        return RecommendationsResponse(**recommendations)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get recommendations: {str(e)}"
        )


# Testing and Validation Endpoints

@app.post("/api/agents/{agent_id}/test", response_model=TestExecutionResponse, tags=["Testing & Validation"])
async def execute_tests(
    agent_id: str,
    request: TestExecutionRequest,
    testing_service: TestingService = Depends(get_testing_service),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    Execute tests for agent implementation
    
    - **agent_id**: Agent identifier
    - **session_id**: Session identifier
    - **test_types**: Optional list of specific test types (security, performance, cost, integration, load)
    
    Returns test execution results with production readiness score
    """
    try:
        # Get workflow data
        workflow_status = await workflow_service.get_workflow_status(agent_id)
        workflow = workflow_service.orchestrator.active_workflows.get(agent_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent workflow not found: {agent_id}"
            )
        
        # Prepare workflow data for testing
        workflow_data = {
            'requirements': workflow.requirements,
            'architecture': workflow.architecture,
            'implementation': workflow.implementation
        }
        
        # Execute tests
        test_results = await testing_service.execute_tests(
            agent_id=agent_id,
            workflow_data=workflow_data,
            test_types=request.test_types
        )
        
        logger.info(f"Tests executed for agent: {agent_id}")
        
        return TestExecutionResponse(**test_results)
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error executing tests: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to execute tests: {str(e)}"
        )


@app.get("/api/agents/{agent_id}/validation", response_model=ValidationReportResponse, tags=["Testing & Validation"])
async def get_validation_report(
    agent_id: str,
    include_details: bool = True,
    testing_service: TestingService = Depends(get_testing_service),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    Get comprehensive validation report
    
    - **agent_id**: Agent identifier
    - **include_details**: Include detailed findings (default: true)
    
    Returns comprehensive validation report with security, performance, cost, and integration analysis
    """
    try:
        # Get workflow data
        workflow = workflow_service.orchestrator.active_workflows.get(agent_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent workflow not found: {agent_id}"
            )
        
        # Prepare workflow data for validation
        workflow_data = {
            'requirements': workflow.requirements,
            'architecture': workflow.architecture,
            'implementation': workflow.implementation
        }
        
        # Get validation report
        validation_report = await testing_service.get_validation_report(
            agent_id=agent_id,
            workflow_data=workflow_data,
            include_details=include_details
        )
        
        logger.info(f"Validation report retrieved for agent: {agent_id}")
        
        return ValidationReportResponse(**validation_report)
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error getting validation report: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get validation report: {str(e)}"
        )


# Export and Deployment Endpoints

@app.get("/api/agents/{agent_id}/export", tags=["Export & Deployment"])
async def export_agent(
    agent_id: str,
    export_format: str = "complete",
    include_tests: bool = True,
    workflow_service: WorkflowService = Depends(get_workflow_service),
    export_service: ExportService = Depends(get_export_service)
):
    """
    Export agent in specified format
    
    - **agent_id**: Agent identifier
    - **export_format**: Export format (code, iac, container, strands, complete)
    - **include_tests**: Include test files (default: true)
    
    Returns export package with all files and metadata
    """
    try:
        # Get workflow data
        workflow = workflow_service.orchestrator.active_workflows.get(agent_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent workflow not found: {agent_id}"
            )
        
        # Prepare workflow data
        workflow_data = {
            'requirements': workflow.requirements,
            'architecture': workflow.architecture,
            'implementation': workflow.implementation
        }
        
        # Validate export format
        try:
            format_enum = ExportFormat(export_format.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid export format: {export_format}. Valid formats: code, iac, container, strands, complete"
            )
        
        # Export agent
        export_package = await export_service.export_agent(
            agent_id=agent_id,
            workflow_data=workflow_data,
            export_format=format_enum,
            include_tests=include_tests
        )
        
        logger.info(f"Agent exported: {agent_id}, format: {export_format}")
        
        return export_package
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error exporting agent: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to export agent: {str(e)}"
        )


@app.get("/api/agents/{agent_id}/export/download", tags=["Export & Deployment"])
async def download_agent_export(
    agent_id: str,
    export_format: str = "complete",
    include_tests: bool = True,
    workflow_service: WorkflowService = Depends(get_workflow_service),
    export_service: ExportService = Depends(get_export_service)
):
    """
    Download agent export as ZIP file
    
    - **agent_id**: Agent identifier
    - **export_format**: Export format (code, iac, container, strands, complete)
    - **include_tests**: Include test files (default: true)
    
    Returns ZIP file download
    """
    try:
        from fastapi.responses import StreamingResponse
        
        # Get workflow data
        workflow = workflow_service.orchestrator.active_workflows.get(agent_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent workflow not found: {agent_id}"
            )
        
        # Prepare workflow data
        workflow_data = {
            'requirements': workflow.requirements,
            'architecture': workflow.architecture,
            'implementation': workflow.implementation
        }
        
        # Validate export format
        try:
            format_enum = ExportFormat(export_format.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid export format: {export_format}"
            )
        
        # Export agent
        export_package = await export_service.export_agent(
            agent_id=agent_id,
            workflow_data=workflow_data,
            export_format=format_enum,
            include_tests=include_tests
        )
        
        # Create ZIP archive
        zip_bytes = await export_service.create_export_archive(export_package)
        
        # Return as downloadable file
        use_case = workflow.requirements.get('use_case', 'agent')
        filename = f"{use_case}_{agent_id[:8]}.zip"
        
        logger.info(f"Agent export downloaded: {agent_id}")
        
        return StreamingResponse(
            io.BytesIO(zip_bytes),
            media_type="application/zip",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error downloading export: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download export: {str(e)}"
        )


class DeploymentRequest(BaseModel):
    session_id: str = Field(..., description="Session identifier")
    deployment_target: str = Field(..., description="Deployment target platform")
    
    class Config:
        schema_extra = {
            "example": {
                "session_id": "session-abc-123",
                "deployment_target": "aws_lambda"
            }
        }


class DeploymentResponse(BaseModel):
    agent_id: str
    deployment_target: str
    scripts: Dict[str, str]
    instructions: str
    estimated_time: str
    
    class Config:
        schema_extra = {
            "example": {
                "agent_id": "agent-abc123",
                "deployment_target": "aws_lambda",
                "scripts": {
                    "deploy.sh": "#!/bin/bash\n...",
                    "deploy.ps1": "# PowerShell\n..."
                },
                "instructions": "Run ./scripts/deploy.sh to deploy",
                "estimated_time": "5-10 minutes"
            }
        }


@app.post("/api/agents/{agent_id}/deploy", response_model=DeploymentResponse, tags=["Export & Deployment"])
async def generate_deployment_scripts(
    agent_id: str,
    request: DeploymentRequest,
    workflow_service: WorkflowService = Depends(get_workflow_service),
    export_service: ExportService = Depends(get_export_service)
):
    """
    Generate deployment scripts for specified target
    
    - **agent_id**: Agent identifier
    - **session_id**: Session identifier
    - **deployment_target**: Target platform (aws_lambda, aws_ecs, aws_fargate, docker, local)
    
    Returns deployment scripts and instructions
    """
    try:
        # Get workflow data
        workflow = workflow_service.orchestrator.active_workflows.get(agent_id)
        
        if not workflow:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Agent workflow not found: {agent_id}"
            )
        
        # Prepare workflow data
        workflow_data = {
            'requirements': workflow.requirements,
            'architecture': workflow.architecture,
            'implementation': workflow.implementation
        }
        
        # Validate deployment target
        try:
            target_enum = DeploymentTarget(request.deployment_target.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid deployment target: {request.deployment_target}. Valid targets: aws_lambda, aws_ecs, aws_fargate, docker, local"
            )
        
        # Generate deployment scripts
        scripts = await export_service.generate_deployment_scripts(
            agent_id=agent_id,
            workflow_data=workflow_data,
            deployment_target=target_enum
        )
        
        # Generate instructions
        instructions = f"""
# Deployment Instructions for {target_enum.value}

1. Ensure AWS credentials are configured:
   ```bash
   aws configure
   ```

2. Run the deployment script:
   ```bash
   ./scripts/deploy-{target_enum.value.replace('_', '-')}.sh
   ```

3. Monitor deployment in AWS Console

4. Test the deployed agent

For detailed instructions, see the README.md file.
"""
        
        # Estimate deployment time
        time_estimates = {
            DeploymentTarget.AWS_LAMBDA: "5-10 minutes",
            DeploymentTarget.AWS_ECS: "10-15 minutes",
            DeploymentTarget.AWS_FARGATE: "10-15 minutes",
            DeploymentTarget.DOCKER: "2-5 minutes",
            DeploymentTarget.LOCAL: "1-2 minutes"
        }
        
        response = DeploymentResponse(
            agent_id=agent_id,
            deployment_target=target_enum.value,
            scripts=scripts,
            instructions=instructions,
            estimated_time=time_estimates.get(target_enum, "5-10 minutes")
        )
        
        logger.info(f"Deployment scripts generated for agent: {agent_id}, target: {target_enum.value}")
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error generating deployment scripts: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate deployment scripts: {str(e)}"
        )


# Error handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            error="Internal Server Error",
            detail=str(exc),
            timestamp=datetime.now(timezone.utc).isoformat()
        ).dict()
    )

# WebSocket Endpoint for Real-Time Updates

@app.websocket("/ws/agents/{agent_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    agent_id: str,
    session_id: Optional[str] = None,
    ws_manager: WebSocketManager = Depends(get_websocket_manager),
    workflow_service: WorkflowService = Depends(get_workflow_service)
):
    """
    WebSocket endpoint for real-time agent workflow updates
    
    - **agent_id**: Agent identifier
    - **session_id**: Optional session identifier (query parameter)
    
    Provides real-time updates for:
    - Workflow phase changes
    - Progress updates
    - AI agent response streaming
    - Error notifications
    
    Supports:
    - Automatic heartbeat (30s interval)
    - Connection timeout (90s)
    - Reconnection with state recovery
    - Multiple concurrent connections per agent
    """
    connection = None
    
    try:
        # Get session_id from query params if not provided
        if not session_id:
            session_id = agent_id  # Use agent_id as fallback
        
        # Connect WebSocket
        connection = await ws_manager.connect(websocket, agent_id, session_id)
        
        logger.info(f"WebSocket connection established: agent_id={agent_id}, session_id={session_id}")
        
        # Check if workflow exists and send state recovery if reconnecting
        try:
            workflow_status = await workflow_service.get_workflow_status(agent_id)
            
            # Send current state for recovery
            state_data = {
                "status": workflow_status.get("status"),
                "progress_percentage": workflow_status.get("progress_percentage"),
                "updated_at": workflow_status.get("updated_at"),
                "message": "State recovered successfully"
            }
            await ws_manager.send_state_recovery(connection, state_data)
            
            logger.info(f"State recovery sent for agent_id={agent_id}")
            
        except ValueError:
            # Workflow doesn't exist yet, that's okay
            logger.debug(f"No existing workflow found for agent_id={agent_id}")
        
        # Message handling loop
        while True:
            try:
                # Receive message from client
                message = await connection.receive_json()
                
                # Handle client message (heartbeat, etc.)
                await ws_manager.handle_client_message(connection, message)
                
            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected normally: agent_id={agent_id}")
                break
            except Exception as e:
                logger.error(f"Error in WebSocket message loop: {e}")
                # Send error to client
                try:
                    await ws_manager.send_error(agent_id, str(e), "MESSAGE_ERROR")
                except:
                    pass
                break
    
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected during setup: agent_id={agent_id}")
    except Exception as e:
        logger.error(f"WebSocket connection error: {e}")
        try:
            await websocket.close(code=1011, reason=str(e))
        except:
            pass
    finally:
        # Clean up connection
        if connection:
            await ws_manager.disconnect(connection)
            logger.info(f"WebSocket cleanup completed: agent_id={agent_id}")


@app.get("/api/websocket/stats", tags=["WebSocket"])
async def get_websocket_stats(
    ws_manager: WebSocketManager = Depends(get_websocket_manager)
):
    """
    Get WebSocket connection statistics
    
    Returns information about active WebSocket connections
    """
    return {
        "total_connections": ws_manager.get_connection_count(),
        "connected_agents": ws_manager.get_connected_agents(),
        "heartbeat_interval": ws_manager.heartbeat_interval,
        "connection_timeout": ws_manager.connection_timeout,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
