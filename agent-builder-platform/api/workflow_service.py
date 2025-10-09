#!/usr/bin/env python3
"""
Agent Creation Workflow Service
Manages agent creation workflow coordination with Manager Agent orchestrator
"""

import logging
import uuid
import sys
import os
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-core'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))

from orchestrator import AgentOrchestrator, UserContext, UserExperienceLevel, WorkflowPhase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WorkflowService:
    """Service for managing agent creation workflows"""
    
    def __init__(self, websocket_manager=None):
        """Initialize workflow service with orchestrator"""
        self.orchestrator = AgentOrchestrator()
        self.websocket_manager = websocket_manager
        logger.info("Workflow service initialized")
    
    async def create_agent_workflow(
        self,
        session_id: str,
        user_id: Optional[str],
        use_case: str,
        description: str,
        experience_level: str = "beginner"
    ) -> Dict[str, Any]:
        """
        Create a new agent creation workflow
        
        Args:
            session_id: Session identifier
            user_id: User identifier (optional)
            use_case: Use case description
            description: Detailed description of requirements
            experience_level: User experience level
            
        Returns:
            Agent workflow details including agent_id
        """
        try:
            # Map experience level string to enum
            exp_level_map = {
                'beginner': UserExperienceLevel.BEGINNER,
                'intermediate': UserExperienceLevel.INTERMEDIATE,
                'advanced': UserExperienceLevel.ADVANCED,
                'expert': UserExperienceLevel.EXPERT
            }
            exp_level = exp_level_map.get(experience_level.lower(), UserExperienceLevel.BEGINNER)
            
            # Create user context
            user_context = UserContext(
                user_id=user_id or f"anonymous-{uuid.uuid4().hex[:8]}",
                session_id=session_id,
                experience_level=exp_level
            )
            
            # Initialize agent creation workflow
            project_id = await self.orchestrator.initialize_agent_creation(
                user_input=description,
                use_case=use_case,
                user_context=user_context
            )
            
            # Get initial workflow status
            status = await self.orchestrator.get_workflow_status(project_id)
            
            logger.info(f"Created agent workflow: {project_id} for session: {session_id}")
            
            result = {
                'agent_id': project_id,
                'session_id': session_id,
                'status': status['current_phase'],
                'progress_percentage': status['progress_percentage'],
                'created_at': status['created_at'],
                'use_case': use_case,
                'description': description,
                'experience_level': experience_level,
                'vector_search_enabled': status.get('vector_search_enabled', False)
            }
            
            # Broadcast workflow creation via WebSocket
            if self.websocket_manager:
                await self.websocket_manager.broadcast_workflow_update(
                    project_id,
                    {
                        'event': 'workflow_created',
                        'use_case': use_case,
                        'status': status['current_phase'],
                        'progress_percentage': status['progress_percentage']
                    }
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to create agent workflow: {e}")
            raise
    
    async def submit_requirements(
        self,
        agent_id: str,
        user_input: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Submit requirements for agent creation
        
        Args:
            agent_id: Agent/project identifier
            user_input: User requirements input
            context: Additional context (budget, timeline, etc.)
            
        Returns:
            Requirements analysis with recommendations
        """
        try:
            # Check if workflow exists
            workflow = self.orchestrator.active_workflows.get(agent_id)
            if not workflow:
                raise ValueError(f"Workflow not found: {agent_id}")
            
            # Consult with AWS Solutions Architect
            analysis = await self.orchestrator.consult_aws_solutions_architect(
                project_id=agent_id,
                user_input=user_input,
                user_context=context or {}
            )
            
            # Get updated workflow status
            status = await self.orchestrator.get_workflow_status(agent_id)
            
            logger.info(f"Requirements submitted for agent: {agent_id}")
            
            result = {
                'agent_id': agent_id,
                'analysis': analysis,
                'current_phase': status['current_phase'],
                'progress_percentage': status['progress_percentage'],
                'updated_at': status['updated_at']
            }
            
            # Broadcast requirements update via WebSocket
            if self.websocket_manager:
                await self.websocket_manager.broadcast_progress_update(
                    agent_id,
                    status['progress_percentage'],
                    status['current_phase'],
                    'Requirements analysis complete'
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to submit requirements: {e}")
            raise
    
    async def process_feedback(
        self,
        agent_id: str,
        feedback_type: str,
        content: str,
        rating: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Process user feedback during workflow
        
        Args:
            agent_id: Agent/project identifier
            feedback_type: Type of feedback (clarification, approval, modification)
            content: Feedback content
            rating: Optional rating 1-5
            
        Returns:
            Feedback processing result
        """
        try:
            # Get current workflow
            workflow = self.orchestrator.active_workflows.get(agent_id)
            if not workflow:
                raise ValueError(f"Workflow not found: {agent_id}")
            
            # Store feedback in workflow
            if 'feedback_history' not in workflow.requirements:
                workflow.requirements['feedback_history'] = []
            
            feedback_entry = {
                'type': feedback_type,
                'content': content,
                'rating': rating,
                'timestamp': datetime.utcnow().isoformat(),
                'phase': workflow.current_phase.value
            }
            workflow.requirements['feedback_history'].append(feedback_entry)
            workflow.updated_at = datetime.utcnow()
            
            # Process based on feedback type
            response = {
                'agent_id': agent_id,
                'feedback_received': True,
                'feedback_type': feedback_type,
                'timestamp': feedback_entry['timestamp']
            }
            
            if feedback_type == 'clarification':
                # User needs clarification - provide more details
                response['action'] = 'clarification_provided'
                response['message'] = 'Thank you for your question. Let me provide more details.'
                
            elif feedback_type == 'approval':
                # User approves current phase - move to next
                old_phase = workflow.current_phase.value
                next_phase = self._get_next_phase(workflow.current_phase)
                response['action'] = 'phase_approved'
                response['message'] = 'Great! Moving to the next phase.'
                response['next_phase'] = next_phase
                
                # Broadcast phase change via WebSocket
                if self.websocket_manager:
                    # Calculate new progress (rough estimate)
                    phase_progress = {
                        'requirements': 20,
                        'architecture': 40,
                        'implementation': 60,
                        'testing': 80,
                        'deployment': 90,
                        'complete': 100
                    }
                    new_progress = phase_progress.get(next_phase, 0)
                    
                    await self.websocket_manager.broadcast_phase_change(
                        agent_id,
                        old_phase,
                        next_phase,
                        new_progress
                    )
                
            elif feedback_type == 'modification':
                # User wants modifications - stay in current phase
                response['action'] = 'modification_requested'
                response['message'] = 'I understand. Let me adjust the recommendations.'
                
            else:
                response['action'] = 'feedback_recorded'
                response['message'] = 'Feedback recorded.'
            
            logger.info(f"Processed feedback for agent: {agent_id}, type: {feedback_type}")
            
            return response
            
        except Exception as e:
            logger.error(f"Failed to process feedback: {e}")
            raise
    
    async def get_workflow_status(self, agent_id: str) -> Dict[str, Any]:
        """
        Get current workflow status
        
        Args:
            agent_id: Agent/project identifier
            
        Returns:
            Current workflow status
        """
        try:
            status = await self.orchestrator.get_workflow_status(agent_id)
            
            return {
                'agent_id': agent_id,
                'status': status['current_phase'],
                'progress_percentage': status['progress_percentage'],
                'completed_steps': status['completed_steps'],
                'active_agents': status['active_agents'],
                'created_at': status['created_at'],
                'updated_at': status['updated_at'],
                'user_context': status['user_context'],
                'vector_search_enabled': status.get('vector_search_enabled', False)
            }
            
        except Exception as e:
            logger.error(f"Failed to get workflow status: {e}")
            raise
    
    async def get_recommendations(
        self,
        agent_id: str,
        recommendation_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get AI recommendations for current phase
        
        Args:
            agent_id: Agent/project identifier
            recommendation_type: Type of recommendations (services, architecture, implementation)
            
        Returns:
            AI recommendations with confidence scores
        """
        try:
            # Get workflow
            workflow = self.orchestrator.active_workflows.get(agent_id)
            if not workflow:
                raise ValueError(f"Workflow not found: {agent_id}")
            
            # Get recommendations based on current phase
            current_phase = workflow.current_phase
            
            recommendations = {
                'agent_id': agent_id,
                'current_phase': current_phase.value,
                'recommendation_type': recommendation_type or 'general',
                'recommendations': [],
                'confidence_score': 0.0,
                'reasoning': '',
                'alternatives': []
            }
            
            # Extract recommendations from workflow state
            if current_phase == WorkflowPhase.REQUIREMENTS:
                if 'aws_architect_analysis' in workflow.requirements:
                    analysis = workflow.requirements['aws_architect_analysis']
                    recommendations['recommendations'] = analysis.get('service_recommendations', [])
                    recommendations['confidence_score'] = analysis.get('confidence_score', 0.0)
                    recommendations['reasoning'] = analysis.get('reasoning', '')
                    
            elif current_phase == WorkflowPhase.ARCHITECTURE:
                if 'architecture' in workflow.architecture:
                    arch = workflow.architecture
                    recommendations['recommendations'] = arch.get('recommendations', [])
                    recommendations['confidence_score'] = arch.get('confidence_score', 0.0)
                    
            elif current_phase == WorkflowPhase.IMPLEMENTATION:
                if 'implementation_plan' in workflow.implementation:
                    impl = workflow.implementation
                    recommendations['recommendations'] = impl.get('recommendations', [])
                    recommendations['confidence_score'] = impl.get('confidence_score', 0.0)
            
            logger.info(f"Retrieved recommendations for agent: {agent_id}, phase: {current_phase.value}")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get recommendations: {e}")
            raise
    
    def _get_next_phase(self, current_phase: WorkflowPhase) -> str:
        """Get the next workflow phase"""
        phase_order = [
            WorkflowPhase.INITIALIZATION,
            WorkflowPhase.REQUIREMENTS,
            WorkflowPhase.ARCHITECTURE,
            WorkflowPhase.IMPLEMENTATION,
            WorkflowPhase.TESTING,
            WorkflowPhase.DEPLOYMENT,
            WorkflowPhase.COMPLETE
        ]
        
        try:
            current_index = phase_order.index(current_phase)
            if current_index < len(phase_order) - 1:
                return phase_order[current_index + 1].value
            return WorkflowPhase.COMPLETE.value
        except ValueError:
            return WorkflowPhase.REQUIREMENTS.value


# Singleton instance
_workflow_service: Optional[WorkflowService] = None


def get_workflow_service(websocket_manager=None) -> WorkflowService:
    """Get workflow service instance (singleton)"""
    global _workflow_service
    if _workflow_service is None:
        _workflow_service = WorkflowService(websocket_manager)
    elif websocket_manager and not _workflow_service.websocket_manager:
        # Update websocket manager if not set
        _workflow_service.websocket_manager = websocket_manager
    return _workflow_service
