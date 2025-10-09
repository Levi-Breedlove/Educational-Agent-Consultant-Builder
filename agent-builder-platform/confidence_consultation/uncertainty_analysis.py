"""
Uncertainty Analysis System

Tracks known-knowns, known-unknowns, and assumed-knowns with confidence
penalty calculation (3% per unknown, 2% per assumption).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class KnowledgeType(Enum):
    """Types of knowledge in uncertainty analysis"""
    KNOWN_KNOWN = "known_known"  # Certainties
    KNOWN_UNKNOWN = "known_unknown"  # Identified gaps
    ASSUMED_KNOWN = "assumed_known"  # Risky assumptions


@dataclass
class UncertaintyAnalysis:
    """
    Tracks different types of knowledge and calculates confidence penalties.
    
    Confidence Penalties:
    - Each known_unknown: -3% confidence
    - Each assumption: -2% confidence
    - Total penalty capped at 20%
    """
    
    known_knowns: List[str] = field(default_factory=list)  # Certainties
    known_unknowns: List[str] = field(default_factory=list)  # Identified gaps
    assumed_knowns: List[str] = field(default_factory=list)  # Risky assumptions
    
    # Penalty rates
    UNKNOWN_PENALTY: float = 0.03  # 3% per unknown
    ASSUMPTION_PENALTY: float = 0.02  # 2% per assumption
    MAX_PENALTY: float = 0.20  # Cap at 20%
    
    def calculate_confidence_penalty(self) -> float:
        """
        Calculate total confidence penalty from uncertainties.
        
        Returns:
            Penalty value (0.0 to 0.20)
        """
        unknown_penalty = len(self.known_unknowns) * self.UNKNOWN_PENALTY
        assumption_penalty = len(self.assumed_knowns) * self.ASSUMPTION_PENALTY
        
        total_penalty = min(self.MAX_PENALTY, unknown_penalty + assumption_penalty)
        
        logger.info(
            f"Uncertainty penalty: {int(total_penalty * 100)}% "
            f"({len(self.known_unknowns)} unknowns, {len(self.assumed_knowns)} assumptions)"
        )
        
        return total_penalty
    
    def get_uncertainty_summary(self) -> Dict[str, Any]:
        """Get summary of uncertainty analysis"""
        return {
            "certainties": len(self.known_knowns),
            "identified_gaps": len(self.known_unknowns),
            "assumptions": len(self.assumed_knowns),
            "confidence_penalty": self.calculate_confidence_penalty(),
            "penalty_breakdown": {
                "from_unknowns": len(self.known_unknowns) * self.UNKNOWN_PENALTY,
                "from_assumptions": len(self.assumed_knowns) * self.ASSUMPTION_PENALTY
            }
        }
    
    def format_for_display(self) -> str:
        """Format uncertainty analysis for user display"""
        penalty = self.calculate_confidence_penalty()
        
        output = [
            f"\n{'='*60}",
            f"UNCERTAINTY ANALYSIS (Penalty: -{int(penalty * 100)}%)",
            f"{'='*60}\n"
        ]
        
        if self.known_knowns:
            output.append("✅ What We Know (Certainties):")
            for item in self.known_knowns:
                output.append(f"  • {item}")
            output.append("")
        
        if self.known_unknowns:
            output.append("❓ What We Don't Know (Gaps to Address):")
            for item in self.known_unknowns:
                output.append(f"  • {item} [-3% confidence]")
            output.append("")
        
        if self.assumed_knowns:
            output.append("⚠️  What We're Assuming (Needs Validation):")
            for item in self.assumed_knowns:
                output.append(f"  • {item} [-2% confidence]")
            output.append("")
        
        output.append(f"{'='*60}\n")
        return "\n".join(output)


class UncertaintyTracker:
    """
    Tracks uncertainties throughout the workflow and proactively identifies
    areas needing clarification.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def track_uncertainties(
        self,
        phase: str,
        analysis: Dict[str, Any]
    ) -> UncertaintyAnalysis:
        """
        Track uncertainties for a specific workflow phase.
        
        Args:
            phase: Current workflow phase (requirements, architecture, etc.)
            analysis: Analysis data for the phase
            
        Returns:
            UncertaintyAnalysis with identified certainties, gaps, and assumptions
        """
        uncertainty = UncertaintyAnalysis()
        
        # Track based on phase
        if phase == "requirements":
            uncertainty = await self._track_requirements_uncertainties(analysis)
        elif phase == "architecture":
            uncertainty = await self._track_architecture_uncertainties(analysis)
        elif phase == "implementation":
            uncertainty = await self._track_implementation_uncertainties(analysis)
        elif phase == "testing":
            uncertainty = await self._track_testing_uncertainties(analysis)
        
        # Log uncertainty summary
        summary = uncertainty.get_uncertainty_summary()
        self.logger.info(
            f"Uncertainty tracking for {phase}: "
            f"{summary['certainties']} certainties, "
            f"{summary['identified_gaps']} gaps, "
            f"{summary['assumptions']} assumptions"
        )
        
        return uncertainty
    
    async def _track_requirements_uncertainties(
        self,
        analysis: Dict[str, Any]
    ) -> UncertaintyAnalysis:
        """Track uncertainties in requirements phase"""
        uncertainty = UncertaintyAnalysis()
        
        # Known knowns (certainties)
        if analysis.get('user_goals'):
            uncertainty.known_knowns.append("User goals clearly stated")
        if analysis.get('use_case'):
            uncertainty.known_knowns.append(f"Use case: {analysis['use_case']}")
        if analysis.get('budget'):
            uncertainty.known_knowns.append(f"Budget: {analysis['budget']}")
        if analysis.get('timeline'):
            uncertainty.known_knowns.append(f"Timeline: {analysis['timeline']}")
        
        # Known unknowns (identified gaps)
        if not analysis.get('expected_load'):
            uncertainty.known_unknowns.append("Expected user load not specified")
        if not analysis.get('data_volume'):
            uncertainty.known_unknowns.append("Data volume requirements unclear")
        if not analysis.get('compliance_requirements'):
            uncertainty.known_unknowns.append("Compliance requirements not specified")
        if not analysis.get('integration_requirements'):
            uncertainty.known_unknowns.append("Integration requirements not defined")
        
        # Assumed knowns (risky assumptions)
        if analysis.get('assumed_load'):
            uncertainty.assumed_knowns.append(
                f"Assuming {analysis['assumed_load']} users/day (needs validation)"
            )
        if analysis.get('assumed_region'):
            uncertainty.assumed_knowns.append(
                f"Assuming {analysis['assumed_region']} AWS region (needs confirmation)"
            )
        if not analysis.get('availability_requirements'):
            uncertainty.assumed_knowns.append(
                "Assuming standard availability (99.9%) without explicit requirement"
            )
        
        return uncertainty
    
    async def _track_architecture_uncertainties(
        self,
        analysis: Dict[str, Any]
    ) -> UncertaintyAnalysis:
        """Track uncertainties in architecture phase"""
        uncertainty = UncertaintyAnalysis()
        
        # Known knowns
        if analysis.get('architecture_pattern'):
            uncertainty.known_knowns.append(
                f"Architecture pattern: {analysis['architecture_pattern']}"
            )
        if analysis.get('aws_services'):
            uncertainty.known_knowns.append(
                f"AWS services selected: {', '.join(analysis['aws_services'])}"
            )
        if analysis.get('cost_estimate'):
            uncertainty.known_knowns.append(
                f"Cost estimate: {analysis['cost_estimate']}"
            )
        
        # Known unknowns
        if not analysis.get('scaling_strategy'):
            uncertainty.known_unknowns.append("Scaling strategy not defined")
        if not analysis.get('disaster_recovery'):
            uncertainty.known_unknowns.append("Disaster recovery plan not specified")
        if not analysis.get('monitoring_strategy'):
            uncertainty.known_unknowns.append("Monitoring strategy not defined")
        
        # Assumed knowns
        if not analysis.get('multi_region'):
            uncertainty.assumed_knowns.append(
                "Assuming single-region deployment (may need multi-region)"
            )
        if not analysis.get('backup_strategy'):
            uncertainty.assumed_knowns.append(
                "Assuming standard backup strategy (needs validation)"
            )
        
        return uncertainty
    
    async def _track_implementation_uncertainties(
        self,
        analysis: Dict[str, Any]
    ) -> UncertaintyAnalysis:
        """Track uncertainties in implementation phase"""
        uncertainty = UncertaintyAnalysis()
        
        # Known knowns
        if analysis.get('code_generated'):
            uncertainty.known_knowns.append("Code generation complete")
        if analysis.get('dependencies_defined'):
            uncertainty.known_knowns.append("Dependencies explicitly defined")
        if analysis.get('security_implemented'):
            uncertainty.known_knowns.append("Security controls implemented")
        
        # Known unknowns
        if not analysis.get('performance_tested'):
            uncertainty.known_unknowns.append("Performance not yet tested")
        if not analysis.get('integration_tested'):
            uncertainty.known_unknowns.append("Integration testing not complete")
        
        # Assumed knowns
        if not analysis.get('error_handling_validated'):
            uncertainty.assumed_knowns.append(
                "Assuming error handling is sufficient (needs validation)"
            )
        
        return uncertainty
    
    async def _track_testing_uncertainties(
        self,
        analysis: Dict[str, Any]
    ) -> UncertaintyAnalysis:
        """Track uncertainties in testing phase"""
        uncertainty = UncertaintyAnalysis()
        
        # Known knowns
        if analysis.get('tests_passed'):
            uncertainty.known_knowns.append(
                f"Tests passed: {analysis['tests_passed']}"
            )
        if analysis.get('security_validated'):
            uncertainty.known_knowns.append("Security validation complete")
        
        # Known unknowns
        if not analysis.get('load_tested'):
            uncertainty.known_unknowns.append("Load testing not performed")
        if not analysis.get('production_validated'):
            uncertainty.known_unknowns.append("Production environment not validated")
        
        return uncertainty
    
    def generate_clarifying_questions(
        self,
        uncertainty: UncertaintyAnalysis
    ) -> List[str]:
        """
        Generate targeted clarifying questions based on uncertainties.
        
        Args:
            uncertainty: UncertaintyAnalysis with identified gaps
            
        Returns:
            List of clarifying questions to ask the user
        """
        questions = []
        
        # Generate questions for known unknowns
        for unknown in uncertainty.known_unknowns:
            if "user load" in unknown.lower():
                questions.append(
                    "How many users do you expect to use this system daily? "
                    "This helps me design the right scaling strategy."
                )
            elif "compliance" in unknown.lower():
                questions.append(
                    "Are there any compliance requirements (HIPAA, PCI-DSS, GDPR) "
                    "I should consider? This affects security architecture."
                )
            elif "data volume" in unknown.lower():
                questions.append(
                    "What's the expected data volume you'll be working with? "
                    "This helps me choose the right storage solution."
                )
            elif "integration" in unknown.lower():
                questions.append(
                    "Do you need to integrate with any existing systems or APIs? "
                    "This affects the architecture design."
                )
        
        # Generate validation questions for assumptions
        for assumption in uncertainty.assumed_knowns:
            if "region" in assumption.lower():
                questions.append(
                    "I'm assuming a single AWS region deployment. "
                    "Do you need multi-region for compliance or availability?"
                )
            elif "availability" in assumption.lower():
                questions.append(
                    "I'm assuming standard availability (99.9%). "
                    "Do you need higher availability guarantees?"
                )
        
        return questions
