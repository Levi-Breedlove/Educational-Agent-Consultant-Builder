"""
Active Listening Service

Implements validation loops that summarize understanding and request user
confirmation before proceeding. Creates regular check-ins at each phase.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class CheckInPhase(Enum):
    """Workflow phases for check-ins"""
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    IMPLEMENTATION = "implementation"
    TESTING = "testing"
    DEPLOYMENT = "deployment"


@dataclass
class UnderstandingValidation:
    """Result of understanding validation"""
    approved: bool
    feedback: Optional[str] = None
    clarifications_needed: List[str] = None
    
    def __post_init__(self):
        if self.clarifications_needed is None:
            self.clarifications_needed = []


@dataclass
class CheckInPrompt:
    """Check-in prompt for a specific phase"""
    phase: CheckInPhase
    summary: str
    key_points: List[str]
    question: str


class ActiveListeningService:
    """
    Implements active listening patterns to ensure user feels heard and consulted.
    
    Key Features:
    - Summarizes understanding before proceeding
    - Requests explicit confirmation
    - Validates interpretation accuracy
    - Regular check-ins at each phase
    - Iterates based on feedback
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def validate_understanding(
        self,
        user_input: str,
        agent_interpretation: Dict[str, Any]
    ) -> UnderstandingValidation:
        """
        Validate understanding before proceeding.
        
        Implements active listening loop:
        1. Summarize what we heard
        2. List key requirements
        3. Ask for confirmation
        4. Iterate if needed
        
        Args:
            user_input: Original user input
            agent_interpretation: Agent's interpretation of the input
            
        Returns:
            UnderstandingValidation with approval status
        """
        # Generate summary
        summary = self._generate_understanding_summary(agent_interpretation)
        
        self.logger.info("Validating understanding with user")
        
        # In a real implementation, this would prompt the user
        # For now, we'll return a structure that can be used by the caller
        return UnderstandingValidation(
            approved=False,  # Requires user confirmation
            feedback=None,
            clarifications_needed=[]
        )
    
    def _generate_understanding_summary(
        self,
        interpretation: Dict[str, Any]
    ) -> str:
        """
        Generate a summary of our understanding.
        
        Args:
            interpretation: Agent's interpretation
            
        Returns:
            Formatted summary for user review
        """
        output = [
            "Let me make sure I understand correctly:\n"
        ]
        
        # Add description
        if interpretation.get('description'):
            output.append(f"**What you want to build:**")
            output.append(f"{interpretation['description']}\n")
        
        # Add key requirements
        if interpretation.get('requirements'):
            output.append("**Key requirements I heard:**")
            for i, req in enumerate(interpretation['requirements'], 1):
                req_text = req if isinstance(req, str) else req.get('description', str(req))
                output.append(f"{i}. {req_text}")
            output.append("")
        
        # Add constraints
        if interpretation.get('constraints'):
            output.append("**Constraints:**")
            for constraint in interpretation['constraints']:
                output.append(f"  • {constraint}")
            output.append("")
        
        # Add goals
        if interpretation.get('goals'):
            output.append("**Your goals:**")
            for goal in interpretation['goals']:
                output.append(f"  → {goal}")
            output.append("")
        
        output.append("Is this accurate? Anything I missed or misunderstood?")
        
        return "\n".join(output)
    
    async def update_understanding(
        self,
        current_interpretation: Dict[str, Any],
        user_feedback: str
    ) -> Dict[str, Any]:
        """
        Update interpretation based on user feedback.
        
        Args:
            current_interpretation: Current interpretation
            user_feedback: User's feedback/corrections
            
        Returns:
            Updated interpretation
        """
        updated = current_interpretation.copy()
        
        # Parse feedback and update interpretation
        # This is a simplified version - real implementation would use NLP
        if "add" in user_feedback.lower():
            self.logger.info("User wants to add information")
            # Add to requirements or constraints
        elif "change" in user_feedback.lower() or "modify" in user_feedback.lower():
            self.logger.info("User wants to modify interpretation")
            # Modify existing items
        elif "remove" in user_feedback.lower():
            self.logger.info("User wants to remove something")
            # Remove items
        
        return updated
    
    def generate_check_in(
        self,
        phase: CheckInPhase,
        output: Dict[str, Any]
    ) -> CheckInPrompt:
        """
        Generate check-in prompt for a specific phase.
        
        Args:
            phase: Current workflow phase
            output: Output from the phase
            
        Returns:
            CheckInPrompt with summary and question
        """
        if phase == CheckInPhase.REQUIREMENTS:
            return self._requirements_check_in(output)
        elif phase == CheckInPhase.ARCHITECTURE:
            return self._architecture_check_in(output)
        elif phase == CheckInPhase.IMPLEMENTATION:
            return self._implementation_check_in(output)
        elif phase == CheckInPhase.TESTING:
            return self._testing_check_in(output)
        elif phase == CheckInPhase.DEPLOYMENT:
            return self._deployment_check_in(output)
        
        return CheckInPrompt(
            phase=phase,
            summary="Phase complete",
            key_points=[],
            question="Does this look good?"
        )
    
    def _requirements_check_in(self, output: Dict[str, Any]) -> CheckInPrompt:
        """Generate check-in for requirements phase"""
        key_points = []
        
        if output.get('use_case'):
            key_points.append(f"Use case: {output['use_case']}")
        if output.get('requirements'):
            key_points.append(f"Requirements identified: {len(output['requirements'])}")
        if output.get('constraints'):
            key_points.append(f"Constraints: {', '.join(output['constraints'][:3])}")
        
        summary = (
            "I've analyzed your requirements and identified what you need. "
            "Before I design the architecture, let me confirm we're aligned."
        )
        
        question = (
            "Does this capture your vision? "
            "Is there anything you'd like to add, change, or clarify?"
        )
        
        return CheckInPrompt(
            phase=CheckInPhase.REQUIREMENTS,
            summary=summary,
            key_points=key_points,
            question=question
        )
    
    def _architecture_check_in(self, output: Dict[str, Any]) -> CheckInPrompt:
        """Generate check-in for architecture phase"""
        key_points = []
        
        if output.get('architecture_pattern'):
            key_points.append(f"Pattern: {output['architecture_pattern']}")
        if output.get('aws_services'):
            services = output['aws_services'][:3]
            key_points.append(f"AWS Services: {', '.join(services)}")
        if output.get('cost_estimate'):
            key_points.append(f"Estimated cost: {output['cost_estimate']}")
        
        summary = (
            "I've designed an architecture that meets your requirements. "
            "Let me make sure this aligns with your expectations before we move to implementation."
        )
        
        question = (
            "Does this architecture design work for you? "
            "Would you like me to explore different service combinations or patterns?"
        )
        
        return CheckInPrompt(
            phase=CheckInPhase.ARCHITECTURE,
            summary=summary,
            key_points=key_points,
            question=question
        )
    
    def _implementation_check_in(self, output: Dict[str, Any]) -> CheckInPrompt:
        """Generate check-in for implementation phase"""
        key_points = []
        
        if output.get('files_generated'):
            key_points.append(f"Files generated: {output['files_generated']}")
        if output.get('security_implemented'):
            key_points.append("Security controls implemented")
        if output.get('monitoring_configured'):
            key_points.append("Monitoring and alerting configured")
        
        summary = (
            "I've generated the implementation code with all necessary components. "
            "Let's review what's been created before we move to testing."
        )
        
        question = (
            "Does this implementation approach work for you? "
            "Would you like me to adjust any technical details or add features?"
        )
        
        return CheckInPrompt(
            phase=CheckInPhase.IMPLEMENTATION,
            summary=summary,
            key_points=key_points,
            question=question
        )
    
    def _testing_check_in(self, output: Dict[str, Any]) -> CheckInPrompt:
        """Generate check-in for testing phase"""
        key_points = []
        
        if output.get('tests_passed'):
            key_points.append(f"Tests passed: {output['tests_passed']}")
        if output.get('security_validated'):
            key_points.append("Security validation complete")
        if output.get('performance_validated'):
            key_points.append("Performance benchmarks met")
        
        summary = (
            "I've validated the implementation through comprehensive testing. "
            "Let's review the results before we prepare for deployment."
        )
        
        question = (
            "Are you comfortable with these test results? "
            "Should we add more validation steps or adjust any thresholds?"
        )
        
        return CheckInPrompt(
            phase=CheckInPhase.TESTING,
            summary=summary,
            key_points=key_points,
            question=question
        )
    
    def _deployment_check_in(self, output: Dict[str, Any]) -> CheckInPrompt:
        """Generate check-in for deployment phase"""
        key_points = []
        
        if output.get('deployment_ready'):
            key_points.append("Deployment package ready")
        if output.get('documentation_complete'):
            key_points.append("Documentation complete")
        if output.get('monitoring_configured'):
            key_points.append("Monitoring dashboards configured")
        
        summary = (
            "Everything is ready for deployment. "
            "Let's review the deployment plan and make sure you're comfortable proceeding."
        )
        
        question = (
            "Are you ready to deploy? "
            "Would you like me to walk through the deployment steps or clarify anything?"
        )
        
        return CheckInPrompt(
            phase=CheckInPhase.DEPLOYMENT,
            summary=summary,
            key_points=key_points,
            question=question
        )
    
    def format_check_in(self, check_in: CheckInPrompt) -> str:
        """
        Format check-in prompt for display.
        
        Args:
            check_in: CheckInPrompt to format
            
        Returns:
            Formatted check-in message
        """
        output = [
            f"\n{'='*60}",
            f"CHECK-IN: {check_in.phase.value.upper()} PHASE",
            f"{'='*60}\n",
            check_in.summary,
            ""
        ]
        
        if check_in.key_points:
            output.append("**Key Points:**")
            for point in check_in.key_points:
                output.append(f"  ✓ {point}")
            output.append("")
        
        output.append(f"**{check_in.question}**")
        output.append(f"\n{'='*60}\n")
        
        return "\n".join(output)
