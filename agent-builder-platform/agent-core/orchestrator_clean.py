#!/usr/bin/env python3
"""
Agent Builder Platform - Core Orchestrator
Coordinates the multi-agent workflow for creating production-ready agents
"""

import json
import logging
import asyncio
import sys
import os
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from enum import Enum
import uuid

# Configure logging first
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WorkflowPhase(Enum):
    """Workflow phases for agent creation"""
    INITIALIZATION = "initialization"
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"
    COMPLETE = "complete"

class UserExperienceLevel(Enum):
    """User experience levels for adaptive guidance"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

@dataclass
class UserContext:
    """User context and preferences"""
    user_id: str
    session_id: str
    experience_level: UserExperienceLevel = UserExperienceLevel.BEGINNER
    preferences: Dict[str, Any] = None
    previous_projects: List[str] = None
    current_project_id: Optional[str] = None
    
    def __post_init__(self):
        if self.preferences is None:
            self.preferences = {}
        if self.previous_projects is None:
            self.previous_projects = []

@dataclass
class WorkflowState:
    """Current state of the agent creation workflow"""
    project_id: str
    current_phase: WorkflowPhase
    completed_steps: List[str]
    active_agents: List[str]
    user_context: UserContext
    requirements: Dict[str, Any] = None
    architecture: Dict[str, Any] = None
    implementation: Dict[str, Any] = None
    test_results: Dict[str, Any] = None
    created_at: datetime = None
    updated_at: datetime = None
    
    def __post_init__(self):
        if self.requirements is None:
            self.requirements = {}
        if self.architecture is None:
            self.architecture = {}
        if self.implementation is None:
            self.implementation = {}
        if self.test_results is None:
            self.test_results = {}
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()

class AgentOrchestrator:
    """
    Core orchestrator that coordinates the multi-agent workflow for creating
    production-ready agents
    """
    
    def __init__(self, project_name: str = "agent-builder-platform", environment: str = "dev"):
        self.project_name = project_name
        self.environment = environment
        
        # Workflow state management
        self.active_workflows: Dict[str, WorkflowState] = {}
        
        # Agent registry (will be populated with specialized agents)
        self.specialized_agents = {}
        
        logger.info(f"Agent Orchestrator initialized for {project_name}-{environment}")

    async def initialize_agent_creation(self, user_input: str, use_case: str, user_context: UserContext) -> str:
        """Initialize a new agent creation workflow"""
        try:
            # Generate unique project ID
            project_id = f"agent-{uuid.uuid4().hex[:8]}"
            
            # Create workflow state
            workflow_state = WorkflowState(
                project_id=project_id,
                current_phase=WorkflowPhase.INITIALIZATION,
                completed_steps=[],
                active_agents=[],
                user_context=user_context
            )
            
            # Store initial requirements
            workflow_state.requirements = {
                'user_input': user_input,
                'use_case': use_case,
                'experience_level': user_context.experience_level.value,
                'created_at': datetime.now().isoformat()
            }
            
            # Register workflow
            self.active_workflows[project_id] = workflow_state
            
            logger.info(f"Initialized agent creation workflow: {project_id}")
            logger.info(f"User input: {user_input[:100]}...")
            logger.info(f"Use case: {use_case}")
            
            # Move to requirements phase
            await self._transition_to_phase(project_id, WorkflowPhase.REQUIREMENTS)
            
            return project_id
            
        except Exception as e:
            logger.error(f"Failed to initialize agent creation: {e}")
            raise

    async def _transition_to_phase(self, project_id: str, new_phase: WorkflowPhase):
        """Transition workflow to a new phase"""
        if project_id not in self.active_workflows:
            raise ValueError(f"Workflow not found: {project_id}")
        
        workflow = self.active_workflows[project_id]
        old_phase = workflow.current_phase
        
        # Update workflow state
        workflow.current_phase = new_phase
        workflow.updated_at = datetime.now()
        
        # Add completed step
        if old_phase != WorkflowPhase.INITIALIZATION:
            workflow.completed_steps.append(old_phase.value)
        
        logger.info(f"Workflow {project_id}: {old_phase.value} -> {new_phase.value}")

    async def get_workflow_status(self, project_id: str) -> Dict[str, Any]:
        """Get current workflow status"""
        if project_id not in self.active_workflows:
            raise ValueError(f"Workflow not found: {project_id}")
        
        workflow = self.active_workflows[project_id]
        
        return {
            'project_id': project_id,
            'current_phase': workflow.current_phase.value,
            'completed_steps': workflow.completed_steps,
            'active_agents': workflow.active_agents,
            'progress_percentage': len(workflow.completed_steps) / 6 * 100,
            'created_at': workflow.created_at.isoformat(),
            'updated_at': workflow.updated_at.isoformat(),
            'user_context': {
                'experience_level': workflow.user_context.experience_level.value,
                'session_id': workflow.user_context.session_id
            }
        }

# Test function
async def test_orchestrator():
    """Test the orchestrator functionality"""
    try:
        print("Testing orchestrator...")
        orchestrator = AgentOrchestrator()
        
        user_context = UserContext(
            user_id="test-user-123",
            session_id="session-456",
            experience_level=UserExperienceLevel.INTERMEDIATE
        )
        
        project_id = await orchestrator.initialize_agent_creation(
            "I want to build a customer support chatbot that can handle high volume and integrate with our existing CRM system",
            "customer_support_chatbot",
            user_context
        )
        
        print(f"Created workflow: {project_id}")
        
        status = await orchestrator.get_workflow_status(project_id)
        print(f"Workflow status: {status['current_phase']} ({status['progress_percentage']:.1f}% complete)")
        
        print("Orchestrator test completed successfully!")
        return True
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_orchestrator())
