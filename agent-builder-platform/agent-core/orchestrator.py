#!/usr/bin/env python3
"""
Agent Builder Platform - Core Orchestrator
Coordinates the multi-agent workflow for creating production-ready agents
Enhanced with vector search capabilities and semantic query understanding
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

# Import specialized agents
try:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
    from aws_solutions_architect import AWSolutionsArchitect
    logger.info("AWS Solutions Architect agent imported successfully")
except ImportError as e:
    logger.warning(f"Failed to import AWS Solutions Architect agent: {e}")
    AWSolutionsArchitect = None

# Import confidence consultation system
try:
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'confidence_consultation'))
    from confidence_consultation import (
        ConfidenceCalculationService,
        UncertaintyTracker,
        MultiSourceValidator,
        ConsultativeCommunicator,
        ActiveListeningService,
        ProgressiveDisclosure,
        MonitoringDashboard,
        CheckInPhase
    )
    logger.info("Confidence consultation system imported successfully")
except ImportError as e:
    logger.warning(f"Failed to import confidence consultation system: {e}")
    ConfidenceCalculationService = None
    UncertaintyTracker = None
    MultiSourceValidator = None
    ConsultativeCommunicator = None
    ActiveListeningService = None
    ProgressiveDisclosure = None
    MonitoringDashboard = None
    CheckInPhase = None

# Temporarily disable enhanced knowledge service import for debugging
EnhancedKnowledgeService = None
SearchStrategy = None
logger.info("Enhanced Knowledge Service disabled for debugging")

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
            self.created_at = datetime.utcnow()
        if self.updated_at is None:
            self.updated_at = datetime.utcnow()

class AgentOrchestrator:
    """
    Core orchestrator that coordinates the multi-agent workflow for creating
    production-ready agents with vector search enhancement
    """
    
    def __init__(self, project_name: str = "agent-builder-platform", environment: str = "dev"):
        self.project_name = project_name
        self.environment = environment
        
        # Workflow state management
        self.active_workflows: Dict[str, WorkflowState] = {}
        
        # Initialize enhanced knowledge service with vector search
        self.knowledge_service = None
        if EnhancedKnowledgeService:
            try:
                self.knowledge_service = EnhancedKnowledgeService(
                    project_name=project_name,
                    environment=environment
                )
                logger.info("Enhanced Knowledge Service initialized with vector search capabilities")
            except Exception as e:
                logger.warning(f"Failed to initialize Enhanced Knowledge Service: {e}")
        
        # Agent registry (will be populated with specialized agents)
        self.specialized_agents = {}
        
        # Initialize confidence consultation system
        self.confidence_service = None
        self.uncertainty_tracker = None
        self.validator = None
        self.communicator = None
        self.listening = None
        self.disclosure = None
        self.dashboard = None
        
        if ConfidenceCalculationService:
            try:
                self.confidence_service = ConfidenceCalculationService()
                self.uncertainty_tracker = UncertaintyTracker()
                self.communicator = ConsultativeCommunicator()
                self.listening = ActiveListeningService()
                self.disclosure = ProgressiveDisclosure()
                self.dashboard = MonitoringDashboard()
                logger.info("Confidence consultation system initialized")
                
                # Multi-source validator will be initialized after knowledge service is ready
                # self.validator = MultiSourceValidator(
                #     mcp_ecosystem=None,  # Will be connected later
                #     vector_search=None,
                #     waf_validator=None,
                #     cost_estimator=None
                # )
            except Exception as e:
                logger.warning(f"Failed to initialize confidence consultation system: {e}")
        
        # Initialize specialized agents
        self._initialize_specialized_agents()
        
        logger.info(f"Agent Orchestrator initialized for {project_name}-{environment}")

    def _initialize_specialized_agents(self):
        """Initialize specialized agents for consultation"""
        try:
            if AWSolutionsArchitect:
                self.specialized_agents['aws_solutions_architect'] = AWSolutionsArchitect(
                    mcp_ecosystem=None,  # Will be connected later
                    knowledge_service=self.knowledge_service
                )
                logger.info("AWS Solutions Architect agent initialized")
            else:
                logger.warning("AWS Solutions Architect agent not available")
        except Exception as e:
            logger.error(f"Failed to initialize specialized agents: {e}")

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
                'created_at': datetime.utcnow().isoformat()
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
        workflow.updated_at = datetime.utcnow()
        
        # Add completed step
        if old_phase != WorkflowPhase.INITIALIZATION:
            workflow.completed_steps.append(old_phase.value)
        
        logger.info(f"Workflow {project_id}: {old_phase.value} → {new_phase.value}")

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
            },
            'vector_search_enabled': self.knowledge_service is not None
        }

    async def consult_aws_solutions_architect(self, project_id: str, user_input: str, user_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Consult with AWS Solutions Architect agent for expert recommendations
        """
        if project_id not in self.active_workflows:
            raise ValueError(f"Workflow not found: {project_id}")
        
        try:
            aws_architect = self.specialized_agents.get('aws_solutions_architect')
            if not aws_architect:
                logger.warning("AWS Solutions Architect agent not available")
                return {
                    'error': 'AWS Solutions Architect agent not available',
                    'confidence_score': 0.0
                }
            
            # Prepare user context
            workflow = self.active_workflows[project_id]
            consultation_context = {
                'experience_level': workflow.user_context.experience_level.value,
                'budget_range': user_context.get('budget_range', 'medium') if user_context else 'medium',
                'project_id': project_id,
                'session_id': workflow.user_context.session_id
            }
            
            # Get expert analysis
            analysis = await aws_architect.analyze_user_requirements(user_input, consultation_context)
            
            # Store analysis in workflow
            workflow.requirements['aws_architect_analysis'] = analysis
            workflow.updated_at = datetime.utcnow()
            
            logger.info(f"AWS Solutions Architect consultation completed with confidence: {analysis.get('confidence_score', 0):.2f}")
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to consult AWS Solutions Architect: {e}")
            return {
                'error': str(e),
                'confidence_score': 0.0,
                'fallback_message': 'Expert consultation temporarily unavailable'
            }

# Test function
async def test_orchestrator():
    """Test the orchestrator functionality with vector search"""
    try:
        print("🚀 Starting orchestrator test...")
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
        
        print(f"✅ Created workflow: {project_id}")
        
        status = await orchestrator.get_workflow_status(project_id)
        print(f"✅ Workflow status: {status['current_phase']} ({status['progress_percentage']:.1f}% complete)")
        print(f"✅ Vector search enabled: {status.get('vector_search_enabled', False)}")
        
        print("🎉 Basic orchestrator test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    async def analyze_requirements_with_vector_search(self, project_id: str, user_query: str) -> Dict[str, Any]:
        """
        Analyze user requirements using semantic vector search to understand intent
        and provide intelligent recommendations
        """
        if project_id not in self.active_workflows:
            raise ValueError(f"Workflow not found: {project_id}")
        
        workflow = self.active_workflows[project_id]
        
        try:
            # Use vector search to understand the query semantically
            if self.knowledge_service:
                # This would use the enhanced knowledge service when available
                search_results = []  # Placeholder for actual vector search
                
                analysis = {
                    'semantic_understanding': {
                        'query_intent': self._analyze_query_intent(user_query),
                        'complexity_level': self._assess_complexity(user_query),
                        'domain_focus': self._identify_domain_focus(user_query)
                    },
                    'recommendations': {
                        'aws_services': [],
                        'agent_patterns': [],
                        'cost_considerations': [],
                        'security_recommendations': []
                    },
                    'confidence_score': 0.9,  # High confidence with vector search
                    'search_metadata': {
                        'total_results': len(search_results),
                        'vector_search_used': True,
                        'fallback_used': False
                    }
                }
            else:
                # Fallback to basic analysis without vector search
                analysis = {
                    'semantic_understanding': {
                        'query_intent': self._analyze_query_intent(user_query),
                        'complexity_level': self._assess_complexity(user_query),
                        'domain_focus': self._identify_domain_focus(user_query)
                    },
                    'recommendations': {
                        'aws_services': [],
                        'agent_patterns': [],
                        'cost_considerations': [],
                        'security_recommendations': []
                    },
                    'confidence_score': 0.6,  # Lower confidence without vector search
                    'search_metadata': {
                        'total_results': 0,
                        'vector_search_used': False,
                        'fallback_used': True
                    }
                }
            
            # Store analysis in workflow state
            workflow.requirements['semantic_analysis'] = analysis
            workflow.updated_at = datetime.utcnow()
            
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze requirements with vector search: {e}")
            # Return basic analysis as fallback
            return {
                'semantic_understanding': {
                    'query_intent': 'general_agent_creation',
                    'complexity_level': 'medium',
                    'domain_focus': 'general'
                },
                'recommendations': {
                    'aws_services': [],
                    'agent_patterns': [],
                    'cost_considerations': [],
                    'security_recommendations': []
                },
                'confidence_score': 0.5,
                'search_metadata': {
                    'total_results': 0,
                    'vector_search_used': False,
                    'fallback_used': True,
                    'error': str(e)
                }
            }

    def _analyze_query_intent(self, query: str) -> str:
        """Analyze the intent behind the user's query"""
        query_lower = query.lower()
        
        if any(term in query_lower for term in ['chatbot', 'chat', 'conversation']):
            return 'chatbot_creation'
        elif any(term in query_lower for term in ['api', 'rest', 'endpoint']):
            return 'api_development'
        elif any(term in query_lower for term in ['data', 'process', 'transform']):
            return 'data_processing'
        elif any(term in query_lower for term in ['monitor', 'alert', 'watch']):
            return 'monitoring_automation'
        elif any(term in query_lower for term in ['deploy', 'ci/cd', 'pipeline']):
            return 'deployment_automation'
        else:
            return 'general_agent_creation'

    def _assess_complexity(self, query: str) -> str:
        """Assess the complexity level of the requested solution"""
        query_lower = query.lower()
        complexity_indicators = {
            'high': ['enterprise', 'scale', 'production', 'multi-region', 'compliance', 'security'],
            'medium': ['integrate', 'connect', 'workflow', 'process', 'automate'],
            'low': ['simple', 'basic', 'quick', 'easy', 'small']
        }
        
        for level, indicators in complexity_indicators.items():
            if any(indicator in query_lower for indicator in indicators):
                return level
        
        return 'medium'  # Default to medium complexity

    def _identify_domain_focus(self, query: str) -> str:
        """Identify the primary domain focus of the query"""
        query_lower = query.lower()
        
        domains = {
            'customer_service': ['customer', 'support', 'help', 'service'],
            'data_analytics': ['data', 'analytics', 'report', 'dashboard'],
            'automation': ['automate', 'workflow', 'process', 'trigger'],
            'integration': ['integrate', 'connect', 'sync', 'api'],
            'monitoring': ['monitor', 'alert', 'watch', 'track'],
            'security': ['security', 'auth', 'permission', 'access']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in query_lower for keyword in keywords):
                return domain
        
        return 'general'

if __name__ == "__main__":
    asyncio.run(test_orchestrator())