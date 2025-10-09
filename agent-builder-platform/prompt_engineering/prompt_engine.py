#!/usr/bin/env python3
"""
Advanced Prompt Engineering Engine
Orchestrates all prompt engineering components for production-ready agent generation
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

try:
    from .prompt_templates import PromptTemplateLibrary, PromptType, SafetyLevel
    from .input_validation import InputValidator, ValidationLevel, ContextualValidator
    from .output_validation import OutputValidator, FindingSeverity
    from .semantic_reasoning import SemanticReasoning, GoalAlignmentValidator, IntentType
except ImportError:
    from prompt_templates import PromptTemplateLibrary, PromptType, SafetyLevel
    from input_validation import InputValidator, ValidationLevel, ContextualValidator
    from output_validation import OutputValidator, FindingSeverity
    from semantic_reasoning import SemanticReasoning, GoalAlignmentValidator, IntentType

logger = logging.getLogger(__name__)

class PromptEngineMode(Enum):
    """Operating modes for prompt engine"""
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STRICT = "strict"

@dataclass
class PromptRequest:
    """Request for prompt generation"""
    user_input: str
    prompt_type: PromptType
    context: Optional[Dict[str, Any]] = None
    user_goals: Optional[List[str]] = None
    safety_level: SafetyLevel = SafetyLevel.STANDARD
    enable_chain_of_thought: bool = True

@dataclass
class PromptResponse:
    """Response from prompt engine"""
    rendered_prompt: str
    validation_passed: bool
    semantic_analysis: Any
    confidence_score: float
    warnings: List[str]
    metadata: Dict[str, Any]

@dataclass
class OutputEvaluation:
    """Evaluation of AI-generated output"""
    is_valid: bool
    security_score: float
    compliance_score: float
    goal_alignment_score: float
    overall_confidence: float
    findings: List[Any]
    recommendations: List[str]
    retry_needed: bool

class AdvancedPromptEngine:
    """
    Advanced prompt engineering engine with multi-layer guardrails
    Implements all 12 requirements from Task 11.10
    """
    
    def __init__(self, mode: PromptEngineMode = PromptEngineMode.PRODUCTION):
        """
        Initialize prompt engine
        
        Args:
            mode: Operating mode (development, production, strict)
        """
        self.mode = mode
        
        # Initialize components
        self.template_library = PromptTemplateLibrary()
        self.input_validator = InputValidator(self._get_validation_level())
        self.contextual_validator = ContextualValidator()
        self.output_validator = OutputValidator()
        self.semantic_reasoner = SemanticReasoning()
        self.goal_validator = GoalAlignmentValidator()
        
        # Metrics tracking
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_validations': 0,
            'retries': 0,
            'average_confidence': 0.0
        }
        
        logger.info(f"Advanced Prompt Engine initialized in {mode.value} mode")
    
    def _get_validation_level(self) -> ValidationLevel:
        """Get validation level based on mode"""
        mode_to_level = {
            PromptEngineMode.DEVELOPMENT: ValidationLevel.STANDARD,
            PromptEngineMode.PRODUCTION: ValidationLevel.STRICT,
            PromptEngineMode.STRICT: ValidationLevel.PARANOID
        }
        return mode_to_level[self.mode]
    
    async def generate_prompt(self, request: PromptRequest) -> PromptResponse:
        """
        Generate a validated, safe prompt with semantic understanding
        
        Implements:
        - Requirement 19.1: Structured prompt templates
        - Requirement 19.2: Multi-layer input validation
        - Requirement 19.5: Semantic reasoning
        - Requirement 19.6: Goal alignment
        
        Args:
            request: PromptRequest with user input and configuration
            
        Returns:
            PromptResponse with rendered prompt and validation results
        """
        self.metrics['total_requests'] += 1
        
        # Step 1: Input validation (Requirement 19.2)
        validation_result = self.input_validator.validate(request.user_input, request.context)
        
        if not validation_result.is_valid and self.mode == PromptEngineMode.STRICT:
            logger.warning(f"Input validation failed: {validation_result.threats_detected}")
            self.metrics['failed_validations'] += 1
            return PromptResponse(
                rendered_prompt="",
                validation_passed=False,
                semantic_analysis=None,
                confidence_score=0.0,
                warnings=[f"Input validation failed: {t.value}" for t in validation_result.threats_detected],
                metadata={'validation_result': asdict(validation_result)}
            )
        
        # Step 2: Semantic analysis (Requirement 19.5)
        semantic_analysis = await self.semantic_reasoner.analyze_intent(
            validation_result.sanitized_input,
            request.context
        )
        
        # Step 3: Get appropriate template (Requirement 19.1)
        template_name = self._map_prompt_type_to_template(request.prompt_type)
        template = self.template_library.get_template(template_name)
        
        if not template:
            logger.error(f"Template not found: {template_name}")
            return PromptResponse(
                rendered_prompt="",
                validation_passed=False,
                semantic_analysis=semantic_analysis,
                confidence_score=0.0,
                warnings=[f"Template not found: {template_name}"],
                metadata={}
            )
        
        # Step 4: Enhance context with semantic insights
        enhanced_context = self._enhance_context(
            request.context or {},
            semantic_analysis
        )
        
        # Step 5: Render prompt with safety measures (Requirement 19.7)
        rendered_prompt = template.render(
            validation_result.sanitized_input,
            enhanced_context
        )
        
        # Step 6: Calculate overall confidence
        confidence_score = self._calculate_confidence(
            validation_result.confidence_score,
            semantic_analysis.confidence_score
        )
        
        # Step 7: Collect warnings
        warnings = validation_result.warnings + semantic_analysis.ambiguities
        
        # Update metrics
        self.metrics['successful_requests'] += 1
        self._update_average_confidence(confidence_score)
        
        return PromptResponse(
            rendered_prompt=rendered_prompt,
            validation_passed=True,
            semantic_analysis=semantic_analysis,
            confidence_score=confidence_score,
            warnings=warnings,
            metadata={
                'template_id': template.template_id,
                'safety_level': template.safety_level.value,
                'intent': semantic_analysis.primary_intent.value,
                'complexity': semantic_analysis.complexity_level.value
            }
        )
    
    async def evaluate_output(
        self,
        output: str,
        original_request: PromptRequest,
        expected_format: Optional[Dict[str, Any]] = None
    ) -> OutputEvaluation:
        """
        Evaluate AI-generated output with comprehensive validation
        
        Implements:
        - Requirement 19.3: Chain-of-thought validation
        - Requirement 19.4: Output validation scanner
        - Requirement 19.6: Goal alignment validation
        - Requirement 19.8: Accuracy enforcement
        - Requirement 19.9: Task completion metrics
        
        Args:
            output: AI-generated output to evaluate
            original_request: Original prompt request
            expected_format: Expected output format
            
        Returns:
            OutputEvaluation with validation results and recommendations
        """
        # Step 1: Output validation (Requirement 19.4)
        validation_result = self.output_validator.validate(output)
        
        # Step 2: Goal alignment validation (Requirement 19.6)
        goal_alignment = None
        if original_request.user_goals:
            try:
                output_dict = json.loads(output) if isinstance(output, str) else output
                goal_alignment = await self.goal_validator.validate_alignment(
                    original_request.user_goals,
                    output_dict,
                    original_request.context
                )
            except json.JSONDecodeError:
                logger.warning("Could not parse output for goal alignment")
        
        # Step 3: Calculate scores
        security_score = validation_result.security_score
        compliance_score = validation_result.compliance_score
        goal_alignment_score = goal_alignment.alignment_score if goal_alignment else 1.0
        
        # Step 4: Calculate overall confidence (Requirement 19.8)
        overall_confidence = self._calculate_output_confidence(
            security_score,
            compliance_score,
            goal_alignment_score,
            validation_result.overall_confidence
        )
        
        # Step 5: Determine if retry needed (Requirement 19.9)
        retry_needed = self._should_retry(
            overall_confidence,
            validation_result,
            goal_alignment
        )
        
        # Step 6: Generate recommendations
        recommendations = self._generate_recommendations(
            validation_result,
            goal_alignment,
            overall_confidence
        )
        
        # Step 7: Determine validity
        is_valid = (
            validation_result.is_valid and
            overall_confidence >= 0.85 and
            not retry_needed
        )
        
        # Update metrics
        if retry_needed:
            self.metrics['retries'] += 1
        
        return OutputEvaluation(
            is_valid=is_valid,
            security_score=security_score,
            compliance_score=compliance_score,
            goal_alignment_score=goal_alignment_score,
            overall_confidence=overall_confidence,
            findings=validation_result.findings,
            recommendations=recommendations,
            retry_needed=retry_needed
        )
    
    def _map_prompt_type_to_template(self, prompt_type: PromptType) -> str:
        """Map prompt type to template name"""
        type_to_template = {
            PromptType.REQUIREMENTS_ANALYSIS: 'requirements_analysis',
            PromptType.ARCHITECTURE_DESIGN: 'architecture_design',
            PromptType.CODE_GENERATION: 'code_generation',
            PromptType.SECURITY_VALIDATION: 'security_validation',
            PromptType.COST_ESTIMATION: 'cost_estimation',
            PromptType.TESTING_STRATEGY: 'testing_strategy'
        }
        return type_to_template.get(prompt_type, 'requirements_analysis')
    
    def _enhance_context(
        self,
        context: Dict[str, Any],
        semantic_analysis: Any
    ) -> Dict[str, Any]:
        """Enhance context with semantic insights"""
        enhanced = context.copy()
        
        enhanced['semantic_insights'] = {
            'primary_intent': semantic_analysis.primary_intent.value,
            'complexity_level': semantic_analysis.complexity_level.value,
            'key_concepts': semantic_analysis.key_concepts,
            'implicit_requirements': semantic_analysis.implicit_requirements
        }
        
        return enhanced
    
    def _calculate_confidence(self, *scores: float) -> float:
        """Calculate overall confidence from multiple scores"""
        if not scores:
            return 0.0
        return sum(scores) / len(scores)
    
    def _calculate_output_confidence(
        self,
        security_score: float,
        compliance_score: float,
        goal_alignment_score: float,
        validation_confidence: float
    ) -> float:
        """Calculate overall output confidence"""
        # Weighted average
        weights = {
            'security': 0.3,
            'compliance': 0.25,
            'goal_alignment': 0.25,
            'validation': 0.2
        }
        
        weighted_score = (
            security_score * weights['security'] +
            compliance_score * weights['compliance'] +
            goal_alignment_score * weights['goal_alignment'] +
            validation_confidence * weights['validation']
        )
        
        return weighted_score
    
    def _should_retry(
        self,
        confidence: float,
        validation_result: Any,
        goal_alignment: Any
    ) -> bool:
        """Determine if output should be retried (Requirement 19.9)"""
        # Retry if confidence below threshold
        if confidence < 0.85:
            return True
        
        # Retry if critical security findings
        critical_findings = [
            f for f in validation_result.findings
            if f.severity == FindingSeverity.CRITICAL
        ]
        if critical_findings:
            return True
        
        # Retry if goal misalignment
        if goal_alignment and not goal_alignment.is_aligned:
            return True
        
        return False
    
    def _generate_recommendations(
        self,
        validation_result: Any,
        goal_alignment: Any,
        confidence: float
    ) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        # Security recommendations
        if validation_result.security_score < 0.8:
            recommendations.append("Address security findings before deployment")
        
        # Compliance recommendations
        if validation_result.compliance_score < 0.8:
            recommendations.append("Review compliance requirements")
        
        # Goal alignment recommendations
        if goal_alignment and goal_alignment.misalignments:
            recommendations.extend(goal_alignment.suggestions)
        
        # Confidence recommendations
        if confidence < 0.85:
            recommendations.append("Increase confidence by addressing validation findings")
        
        # Critical findings
        critical_findings = [
            f for f in validation_result.findings
            if f.severity == FindingSeverity.CRITICAL
        ]
        if critical_findings:
            recommendations.append(f"CRITICAL: Address {len(critical_findings)} critical security issues")
        
        return recommendations
    
    def _update_average_confidence(self, new_confidence: float):
        """Update running average confidence"""
        total = self.metrics['successful_requests']
        current_avg = self.metrics['average_confidence']
        
        self.metrics['average_confidence'] = (
            (current_avg * (total - 1) + new_confidence) / total
        )
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get engine metrics (Requirement 19.9)"""
        success_rate = (
            self.metrics['successful_requests'] / self.metrics['total_requests']
            if self.metrics['total_requests'] > 0 else 0.0
        )
        
        return {
            **self.metrics,
            'success_rate': success_rate,
            'first_attempt_success_rate': 1.0 - (self.metrics['retries'] / max(1, self.metrics['successful_requests']))
        }
    
    def reset_metrics(self):
        """Reset metrics"""
        self.metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'failed_validations': 0,
            'retries': 0,
            'average_confidence': 0.0
        }


# Convenience functions for common use cases

async def generate_requirements_prompt(user_input: str, context: Optional[Dict[str, Any]] = None) -> PromptResponse:
    """Generate requirements analysis prompt"""
    engine = AdvancedPromptEngine()
    request = PromptRequest(
        user_input=user_input,
        prompt_type=PromptType.REQUIREMENTS_ANALYSIS,
        context=context,
        safety_level=SafetyLevel.STANDARD
    )
    return await engine.generate_prompt(request)


async def generate_code_prompt(user_input: str, context: Optional[Dict[str, Any]] = None) -> PromptResponse:
    """Generate code generation prompt with critical safety"""
    engine = AdvancedPromptEngine()
    request = PromptRequest(
        user_input=user_input,
        prompt_type=PromptType.CODE_GENERATION,
        context=context,
        safety_level=SafetyLevel.CRITICAL
    )
    return await engine.generate_prompt(request)


async def validate_generated_code(code: str, original_request: PromptRequest) -> OutputEvaluation:
    """Validate generated code"""
    engine = AdvancedPromptEngine()
    return await engine.evaluate_output(code, original_request)
