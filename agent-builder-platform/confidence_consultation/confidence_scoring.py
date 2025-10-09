"""
Enhanced Confidence Scoring System

Implements multi-factor weighted confidence scoring with 95% baseline enforcement.
Agents refuse to respond if confidence falls below the baseline threshold.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class ConfidenceFactor(Enum):
    """Individual confidence factors with their weights"""
    INFORMATION_COMPLETENESS = ("information_completeness", 0.25)
    REQUIREMENT_CLARITY = ("requirement_clarity", 0.20)
    TECHNICAL_FEASIBILITY = ("technical_feasibility", 0.20)
    VALIDATION_COVERAGE = ("validation_coverage", 0.15)
    RISK_ASSESSMENT = ("risk_assessment", 0.10)
    USER_ALIGNMENT = ("user_alignment", 0.10)
    
    def __init__(self, key: str, weight: float):
        self.key = key
        self.weight = weight


@dataclass
class EnhancedConfidenceScore:
    """
    Multi-factor confidence score with transparency and baseline enforcement.
    
    Confidence Factors (weighted):
    - Information Completeness: 25% - Do we have all needed information?
    - Requirement Clarity: 20% - Are requirements clear and unambiguous?
    - Technical Feasibility: 20% - Can we build this with available resources?
    - Validation Coverage: 15% - Have we validated all assumptions?
    - Risk Assessment: 10% - What are the identified risks?
    - User Alignment: 10% - Does this match user goals?
    """
    
    # Core factors (0.0 to 1.0)
    information_completeness: float
    requirement_clarity: float
    technical_feasibility: float
    validation_coverage: float
    risk_assessment: float
    user_alignment: float
    
    # Composite score (weighted average)
    overall_confidence: float
    
    # Transparency
    confidence_boosters: List[str] = field(default_factory=list)
    uncertainty_factors: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    
    # Metadata
    calculation_timestamp: str = ""
    phase: str = ""
    
    # Baseline threshold
    BASELINE_THRESHOLD: float = 0.95
    BOOST_CAP: float = 0.98
    
    def meets_baseline(self) -> bool:
        """Check if confidence meets the 95% baseline threshold"""
        return self.overall_confidence >= self.BASELINE_THRESHOLD
    
    def get_confidence_breakdown(self) -> Dict[str, float]:
        """Get detailed breakdown of confidence factors"""
        return {
            "Information Completeness (25%)": self.information_completeness,
            "Requirement Clarity (20%)": self.requirement_clarity,
            "Technical Feasibility (20%)": self.technical_feasibility,
            "Validation Coverage (15%)": self.validation_coverage,
            "Risk Assessment (10%)": self.risk_assessment,
            "User Alignment (10%)": self.user_alignment,
            "Overall Confidence": self.overall_confidence
        }
    
    def format_for_display(self) -> str:
        """Format confidence score for user display"""
        percentage = int(self.overall_confidence * 100)
        status = "✅ MEETS BASELINE" if self.meets_baseline() else "⚠️ BELOW BASELINE"
        
        output = [
            f"\n{'='*60}",
            f"CONFIDENCE SCORE: {percentage}% {status}",
            f"{'='*60}\n",
            "Confidence Breakdown:",
        ]
        
        for factor, score in self.get_confidence_breakdown().items():
            if factor != "Overall Confidence":
                bar = "█" * int(score * 20)
                output.append(f"  {factor}: {int(score * 100)}% {bar}")
        
        if self.confidence_boosters:
            output.append("\n✨ What Increases Confidence:")
            for booster in self.confidence_boosters:
                output.append(f"  + {booster}")
        
        if self.uncertainty_factors:
            output.append("\n⚠️  Uncertainty Factors:")
            for factor in self.uncertainty_factors:
                output.append(f"  - {factor}")
        
        if self.recommended_actions:
            output.append("\n💡 Recommended Actions:")
            for action in self.recommended_actions:
                output.append(f"  → {action}")
        
        output.append(f"\n{'='*60}\n")
        return "\n".join(output)


class ConfidenceCalculationService:
    """
    Service for calculating multi-factor confidence scores with baseline enforcement.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    async def calculate_confidence(
        self,
        analysis: Dict[str, Any],
        phase: str = "general"
    ) -> EnhancedConfidenceScore:
        """
        Calculate multi-factor confidence score.
        
        Args:
            analysis: Analysis data containing requirements, architecture, etc.
            phase: Current workflow phase
            
        Returns:
            EnhancedConfidenceScore with detailed breakdown
        """
        from datetime import datetime
        
        # Calculate each factor
        factors = {
            'information_completeness': self._assess_information_completeness(analysis),
            'requirement_clarity': self._assess_requirement_clarity(analysis),
            'technical_feasibility': self._assess_technical_feasibility(analysis),
            'validation_coverage': self._assess_validation_coverage(analysis),
            'risk_assessment': self._assess_risks(analysis),
            'user_alignment': self._assess_user_alignment(analysis)
        }
        
        # Calculate weighted average
        overall_confidence = sum(
            factors[factor.key] * factor.weight
            for factor in ConfidenceFactor
        )
        
        # Identify boosters and uncertainties
        confidence_boosters = self._identify_boosters(factors, analysis)
        uncertainty_factors = self._identify_uncertainties(factors, analysis)
        recommended_actions = self._generate_actions(uncertainty_factors, factors)
        
        score = EnhancedConfidenceScore(
            information_completeness=factors['information_completeness'],
            requirement_clarity=factors['requirement_clarity'],
            technical_feasibility=factors['technical_feasibility'],
            validation_coverage=factors['validation_coverage'],
            risk_assessment=factors['risk_assessment'],
            user_alignment=factors['user_alignment'],
            overall_confidence=overall_confidence,
            confidence_boosters=confidence_boosters,
            uncertainty_factors=uncertainty_factors,
            recommended_actions=recommended_actions,
            calculation_timestamp=datetime.utcnow().isoformat(),
            phase=phase
        )
        
        # Log confidence calculation
        self.logger.info(
            f"Confidence calculated: {int(overall_confidence * 100)}% "
            f"(baseline: {'MET' if score.meets_baseline() else 'NOT MET'})"
        )
        
        return score
    
    def _assess_information_completeness(self, analysis: Dict[str, Any]) -> float:
        """Assess if we have all needed information (25% weight)"""
        score = 0.5  # Base score
        
        # Check for key information
        if analysis.get('user_goals'):
            score += 0.15
        if analysis.get('requirements'):
            score += 0.15
        if analysis.get('constraints'):
            score += 0.10
        if analysis.get('success_criteria'):
            score += 0.10
        
        return min(1.0, score)
    
    def _assess_requirement_clarity(self, analysis: Dict[str, Any]) -> float:
        """Assess if requirements are clear and unambiguous (20% weight)"""
        score = 0.5  # Base score
        
        requirements = analysis.get('requirements', [])
        if not requirements:
            return 0.3
        
        # Check requirement quality
        clear_requirements = sum(
            1 for req in requirements
            if len(req.get('description', '')) > 20  # Has detailed description
        )
        
        if clear_requirements > 0:
            score += 0.3 * (clear_requirements / len(requirements))
        
        # Check for acceptance criteria
        if any(req.get('acceptance_criteria') for req in requirements):
            score += 0.2
        
        return min(1.0, score)
    
    def _assess_technical_feasibility(self, analysis: Dict[str, Any]) -> float:
        """Assess if solution is technically feasible (20% weight)"""
        score = 0.6  # Base score (assume feasible unless proven otherwise)
        
        # Check for technical constraints
        if analysis.get('aws_services'):
            score += 0.15
        if analysis.get('architecture_pattern'):
            score += 0.15
        if not analysis.get('technical_blockers'):
            score += 0.10
        
        return min(1.0, score)
    
    def _assess_validation_coverage(self, analysis: Dict[str, Any]) -> float:
        """Assess if assumptions have been validated (15% weight)"""
        score = 0.4  # Base score
        
        # Check validation activities
        if analysis.get('validated_assumptions'):
            score += 0.20
        if analysis.get('mcp_validation'):
            score += 0.20
        if analysis.get('cost_validation'):
            score += 0.10
        if analysis.get('security_validation'):
            score += 0.10
        
        return min(1.0, score)
    
    def _assess_risks(self, analysis: Dict[str, Any]) -> float:
        """Assess identified risks (10% weight)"""
        score = 0.7  # Base score
        
        risks = analysis.get('risks', [])
        
        # Lower score if high-severity risks exist
        high_severity_risks = sum(
            1 for risk in risks
            if risk.get('severity') == 'high'
        )
        
        if high_severity_risks > 0:
            score -= 0.15 * min(high_severity_risks, 3)
        
        # Increase score if risks have mitigation plans
        mitigated_risks = sum(
            1 for risk in risks
            if risk.get('mitigation')
        )
        
        if risks and mitigated_risks == len(risks):
            score += 0.15
        
        return max(0.3, min(1.0, score))
    
    def _assess_user_alignment(self, analysis: Dict[str, Any]) -> float:
        """Assess alignment with user goals (10% weight)"""
        score = 0.5  # Base score
        
        # Check for explicit user confirmation
        if analysis.get('user_confirmed'):
            score += 0.25
        if analysis.get('user_feedback_incorporated'):
            score += 0.15
        if analysis.get('goals_mapped_to_requirements'):
            score += 0.10
        
        return min(1.0, score)
    
    def _identify_boosters(
        self,
        factors: Dict[str, float],
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify what increases confidence"""
        boosters = []
        
        if factors['information_completeness'] > 0.85:
            boosters.append("Complete information provided")
        if factors['requirement_clarity'] > 0.85:
            boosters.append("Clear, well-defined requirements")
        if factors['technical_feasibility'] > 0.85:
            boosters.append("Technically feasible with proven patterns")
        if factors['validation_coverage'] > 0.80:
            boosters.append("Assumptions validated across multiple sources")
        if factors['risk_assessment'] > 0.80:
            boosters.append("Risks identified and mitigated")
        if factors['user_alignment'] > 0.85:
            boosters.append("Strong alignment with user goals")
        
        if analysis.get('mcp_validation'):
            boosters.append("Cross-validated with MCP knowledge sources")
        if analysis.get('vector_search_results'):
            boosters.append("Semantic understanding confirmed")
        if analysis.get('waf_compliance'):
            boosters.append("Aligned with AWS Well-Architected Framework")
        
        return boosters
    
    def _identify_uncertainties(
        self,
        factors: Dict[str, float],
        analysis: Dict[str, Any]
    ) -> List[str]:
        """Identify what reduces confidence"""
        uncertainties = []
        
        if factors['information_completeness'] < 0.70:
            uncertainties.append("Missing key information")
        if factors['requirement_clarity'] < 0.70:
            uncertainties.append("Requirements need clarification")
        if factors['technical_feasibility'] < 0.70:
            uncertainties.append("Technical feasibility uncertain")
        if factors['validation_coverage'] < 0.60:
            uncertainties.append("Assumptions not fully validated")
        if factors['risk_assessment'] < 0.60:
            uncertainties.append("High-severity risks identified")
        if factors['user_alignment'] < 0.70:
            uncertainties.append("User alignment needs confirmation")
        
        return uncertainties
    
    def _generate_actions(
        self,
        uncertainties: List[str],
        factors: Dict[str, float]
    ) -> List[str]:
        """Generate recommended actions to improve confidence"""
        actions = []
        
        if factors['information_completeness'] < 0.85:
            actions.append("Gather additional information about requirements and constraints")
        if factors['requirement_clarity'] < 0.85:
            actions.append("Clarify ambiguous requirements with specific examples")
        if factors['validation_coverage'] < 0.80:
            actions.append("Validate assumptions with MCP sources and vector search")
        if factors['user_alignment'] < 0.85:
            actions.append("Confirm understanding with user before proceeding")
        
        return actions
