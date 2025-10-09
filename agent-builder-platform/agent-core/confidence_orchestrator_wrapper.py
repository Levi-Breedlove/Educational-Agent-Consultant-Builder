"""
Confidence-Enhanced Orchestrator Wrapper

Wraps the base orchestrator with confidence consultation features:
- 95% confidence baseline enforcement
- Consultative communication
- Active listening and check-ins
- Progressive disclosure
- Real-time confidence monitoring
"""

import logging
from typing import Dict, Any, Optional
from orchestrator import AgentOrchestrator, WorkflowPhase, UserContext

logger = logging.getLogger(__name__)


class ConfidenceEnhancedOrchestrator(AgentOrchestrator):
    """
    Enhanced orchestrator with integrated confidence consultation system.
    
    Wraps all phase methods with:
    - Confidence calculation and baseline enforcement
    - Uncertainty tracking and clarification
    - Consultative communication transformation
    - Active listening check-ins
    - Experience level adaptation
    - Real-time confidence monitoring
    """
    
    async def execute_requirements_phase(self, project_id: str, user_input: str) -> Dict[str, Any]:
        """
        Execute requirements phase with confidence integration.
        
        Returns:
            Dict with 'status', 'content', 'confidence', 'check_in', 'needs_clarification'
        """
        if not self.confidence_service:
            # Fallback to basic execution if confidence system not available
            return await self._execute_requirements_basic(project_id, user_input)
        
        try:
            # 1. Detect user experience level
            experience_level = self.disclosure.detect_experience_level(user_input)
            logger.info(f"Detected experience level: {experience_level.value}")
            
            # 2. Process requirements (existing logic)
            requirements = await self._process_requirements(project_id, user_input)
            
            # 3. Calculate confidence
            score = await self.confidence_service.calculate_confidence(
                requirements, phase='requirements'
            )
            logger.info(f"Requirements confidence: {int(score.overall_confidence * 100)}%")
            
            # 4. Track uncertainties
            uncertainty = await self.uncertainty_tracker.track_uncertainties(
                'requirements', requirements
            )
            
            # Apply uncertainty penalty
            penalty = uncertainty.calculate_confidence_penalty()
            adjusted_confidence = max(0, score.overall_confidence - penalty)
            
            # 5. Check if baseline met
            if adjusted_confidence < 0.95:
                logger.warning(f"Confidence below baseline: {int(adjusted_confidence * 100)}%")
                
                # Generate clarifying questions
                questions = self.uncertainty_tracker.generate_clarifying_questions(uncertainty)
                
                return {
                    'status': 'needs_clarification',
                    'confidence': adjusted_confidence,
                    'questions': questions,
                    'uncertainty_analysis': uncertainty.format_for_display(),
                    'confidence_breakdown': score.format_for_display()
                }
            
            # 6. Apply consultative communication
            consultative_content = self.communicator.format_consultative_response(
                requirements, score
            )
            
            # 7. Adapt to experience level
            adapted = self.disclosure.adapt_content(
                consultative_content, experience_level
            )
            
            # 8. Generate check-in
            from confidence_consultation import CheckInPhase
            check_in = self.listening.generate_check_in(
                CheckInPhase.REQUIREMENTS, requirements
            )
            
            # 9. Monitor confidence
            self.dashboard.track_confidence(project_id, 'requirements', adjusted_confidence)
            
            # 10. Return enhanced response
            return {
                'status': 'success',
                'content': adapted,
                'confidence': adjusted_confidence,
                'confidence_breakdown': score.get_confidence_breakdown(),
                'check_in': self.listening.format_check_in(check_in),
                'experience_level': experience_level.value,
                'phase': 'requirements'
            }
            
        except Exception as e:
            logger.error(f"Error in confidence-enhanced requirements phase: {e}")
            # Fallback to basic execution
            return await self._execute_requirements_basic(project_id, user_input)
    
    async def execute_architecture_phase(self, project_id: str) -> Dict[str, Any]:
        """Execute architecture phase with confidence integration."""
        if not self.confidence_service:
            return await self._execute_architecture_basic(project_id)
        
        try:
            # 1. Process architecture (existing logic)
            architecture = await self._process_architecture(project_id)
            
            # 2. Calculate confidence
            score = await self.confidence_service.calculate_confidence(
                architecture, phase='architecture'
            )
            
            # 3. Track uncertainties
            uncertainty = await self.uncertainty_tracker.track_uncertainties(
                'architecture', architecture
            )
            
            penalty = uncertainty.calculate_confidence_penalty()
            adjusted_confidence = max(0, score.overall_confidence - penalty)
            
            # 4. Check baseline
            if adjusted_confidence < 0.95:
                questions = self.uncertainty_tracker.generate_clarifying_questions(uncertainty)
                return {
                    'status': 'needs_clarification',
                    'confidence': adjusted_confidence,
                    'questions': questions
                }
            
            # 5. Apply consultative communication
            consultative_content = self.communicator.format_consultative_response(
                architecture, score
            )
            
            # 6. Generate check-in
            from confidence_consultation import CheckInPhase
            check_in = self.listening.generate_check_in(
                CheckInPhase.ARCHITECTURE, architecture
            )
            
            # 7. Monitor
            self.dashboard.track_confidence(project_id, 'architecture', adjusted_confidence)
            
            return {
                'status': 'success',
                'content': consultative_content,
                'confidence': adjusted_confidence,
                'check_in': self.listening.format_check_in(check_in),
                'phase': 'architecture'
            }
            
        except Exception as e:
            logger.error(f"Error in confidence-enhanced architecture phase: {e}")
            return await self._execute_architecture_basic(project_id)
    
    async def execute_implementation_phase(self, project_id: str) -> Dict[str, Any]:
        """Execute implementation phase with confidence integration."""
        if not self.confidence_service:
            return await self._execute_implementation_basic(project_id)
        
        try:
            implementation = await self._process_implementation(project_id)
            
            score = await self.confidence_service.calculate_confidence(
                implementation, phase='implementation'
            )
            
            uncertainty = await self.uncertainty_tracker.track_uncertainties(
                'implementation', implementation
            )
            
            penalty = uncertainty.calculate_confidence_penalty()
            adjusted_confidence = max(0, score.overall_confidence - penalty)
            
            if adjusted_confidence < 0.95:
                questions = self.uncertainty_tracker.generate_clarifying_questions(uncertainty)
                return {
                    'status': 'needs_clarification',
                    'confidence': adjusted_confidence,
                    'questions': questions
                }
            
            consultative_content = self.communicator.format_consultative_response(
                implementation, score
            )
            
            from confidence_consultation import CheckInPhase
            check_in = self.listening.generate_check_in(
                CheckInPhase.IMPLEMENTATION, implementation
            )
            
            self.dashboard.track_confidence(project_id, 'implementation', adjusted_confidence)
            
            return {
                'status': 'success',
                'content': consultative_content,
                'confidence': adjusted_confidence,
                'check_in': self.listening.format_check_in(check_in),
                'phase': 'implementation'
            }
            
        except Exception as e:
            logger.error(f"Error in confidence-enhanced implementation phase: {e}")
            return await self._execute_implementation_basic(project_id)
    
    async def execute_testing_phase(self, project_id: str) -> Dict[str, Any]:
        """Execute testing phase with confidence integration."""
        if not self.confidence_service:
            return await self._execute_testing_basic(project_id)
        
        try:
            testing = await self._process_testing(project_id)
            
            score = await self.confidence_service.calculate_confidence(
                testing, phase='testing'
            )
            
            uncertainty = await self.uncertainty_tracker.track_uncertainties(
                'testing', testing
            )
            
            penalty = uncertainty.calculate_confidence_penalty()
            adjusted_confidence = max(0, score.overall_confidence - penalty)
            
            if adjusted_confidence < 0.95:
                questions = self.uncertainty_tracker.generate_clarifying_questions(uncertainty)
                return {
                    'status': 'needs_clarification',
                    'confidence': adjusted_confidence,
                    'questions': questions
                }
            
            consultative_content = self.communicator.format_consultative_response(
                testing, score
            )
            
            from confidence_consultation import CheckInPhase
            check_in = self.listening.generate_check_in(
                CheckInPhase.TESTING, testing
            )
            
            self.dashboard.track_confidence(project_id, 'testing', adjusted_confidence)
            
            return {
                'status': 'success',
                'content': consultative_content,
                'confidence': adjusted_confidence,
                'check_in': self.listening.format_check_in(check_in),
                'phase': 'testing'
            }
            
        except Exception as e:
            logger.error(f"Error in confidence-enhanced testing phase: {e}")
            return await self._execute_testing_basic(project_id)
    
    def get_confidence_dashboard(self, project_id: str) -> Dict[str, Any]:
        """Get confidence dashboard for a project."""
        if not self.dashboard:
            return {'error': 'Confidence monitoring not available'}
        
        try:
            summary = self.dashboard.get_session_summary(project_id)
            dashboard_text = self.dashboard.format_dashboard(project_id)
            
            return {
                'summary': summary,
                'dashboard': dashboard_text,
                'status': 'success'
            }
        except Exception as e:
            logger.error(f"Error getting confidence dashboard: {e}")
            return {'error': str(e)}
    
    # Fallback methods (basic execution without confidence)
    async def _execute_requirements_basic(self, project_id: str, user_input: str) -> Dict[str, Any]:
        """Basic requirements execution without confidence features."""
        requirements = await self._process_requirements(project_id, user_input)
        return {
            'status': 'success',
            'content': str(requirements),
            'phase': 'requirements'
        }
    
    async def _execute_architecture_basic(self, project_id: str) -> Dict[str, Any]:
        """Basic architecture execution without confidence features."""
        architecture = await self._process_architecture(project_id)
        return {
            'status': 'success',
            'content': str(architecture),
            'phase': 'architecture'
        }
    
    async def _execute_implementation_basic(self, project_id: str) -> Dict[str, Any]:
        """Basic implementation execution without confidence features."""
        implementation = await self._process_implementation(project_id)
        return {
            'status': 'success',
            'content': str(implementation),
            'phase': 'implementation'
        }
    
    async def _execute_testing_basic(self, project_id: str) -> Dict[str, Any]:
        """Basic testing execution without confidence features."""
        testing = await self._process_testing(project_id)
        return {
            'status': 'success',
            'content': str(testing),
            'phase': 'testing'
        }
    
    # Placeholder methods for actual processing (to be implemented)
    async def _process_requirements(self, project_id: str, user_input: str) -> Dict[str, Any]:
        """Process requirements - placeholder for actual implementation."""
        workflow = self.active_workflows.get(project_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {project_id}")
        
        # This would call the actual requirements processing logic
        return {
            'user_input': user_input,
            'requirements': [],
            'use_case': workflow.requirements.get('use_case', 'general')
        }
    
    async def _process_architecture(self, project_id: str) -> Dict[str, Any]:
        """Process architecture - placeholder for actual implementation."""
        workflow = self.active_workflows.get(project_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {project_id}")
        
        return {
            'architecture_pattern': 'serverless',
            'aws_services': []
        }
    
    async def _process_implementation(self, project_id: str) -> Dict[str, Any]:
        """Process implementation - placeholder for actual implementation."""
        workflow = self.active_workflows.get(project_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {project_id}")
        
        return {
            'files_generated': 0,
            'code': []
        }
    
    async def _process_testing(self, project_id: str) -> Dict[str, Any]:
        """Process testing - placeholder for actual implementation."""
        workflow = self.active_workflows.get(project_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {project_id}")
        
        return {
            'tests_passed': 0,
            'tests_failed': 0
        }
