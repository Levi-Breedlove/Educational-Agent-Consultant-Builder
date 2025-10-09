#!/usr/bin/env python3
"""
Semantic Reasoning System
Uses vector embeddings for intent understanding and semantic query analysis
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class IntentType(Enum):
    """Types of user intents"""
    REQUIREMENTS_GATHERING = "requirements_gathering"
    ARCHITECTURE_DESIGN = "architecture_design"
    CODE_GENERATION = "code_generation"
    COST_OPTIMIZATION = "cost_optimization"
    SECURITY_REVIEW = "security_review"
    TROUBLESHOOTING = "troubleshooting"
    CLARIFICATION = "clarification"
    UNKNOWN = "unknown"

class ComplexityLevel(Enum):
    """Complexity levels for requests"""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    EXPERT = "expert"

@dataclass
class SemanticAnalysis:
    """Result of semantic analysis"""
    primary_intent: IntentType
    secondary_intents: List[IntentType]
    complexity_level: ComplexityLevel
    key_concepts: List[str]
    implicit_requirements: List[str]
    ambiguities: List[str]
    confidence_score: float
    reasoning: str

@dataclass
class GoalAlignment:
    """Goal alignment validation result"""
    is_aligned: bool
    user_goals: List[str]
    recommendation_goals: List[str]
    alignment_score: float
    misalignments: List[str]
    suggestions: List[str]

class SemanticReasoning:
    """Semantic reasoning engine for intent understanding"""
    
    # Intent keywords mapping
    INTENT_KEYWORDS = {
        IntentType.REQUIREMENTS_GATHERING: [
            'need', 'want', 'require', 'should', 'must', 'looking for',
            'help me', 'build', 'create', 'develop', 'design'
        ],
        IntentType.ARCHITECTURE_DESIGN: [
            'architecture', 'design', 'structure', 'components', 'services',
            'scalable', 'reliable', 'available', 'distributed'
        ],
        IntentType.CODE_GENERATION: [
            'code', 'implement', 'function', 'class', 'script', 'program',
            'write', 'generate', 'create code', 'lambda', 'api'
        ],
        IntentType.COST_OPTIMIZATION: [
            'cost', 'price', 'budget', 'cheap', 'affordable', 'free tier',
            'optimize cost', 'reduce cost', 'save money', 'expensive'
        ],
        IntentType.SECURITY_REVIEW: [
            'security', 'secure', 'safe', 'protect', 'encryption', 'iam',
            'vulnerability', 'compliance', 'audit', 'access control'
        ],
        IntentType.TROUBLESHOOTING: [
            'error', 'issue', 'problem', 'not working', 'failed', 'broken',
            'debug', 'fix', 'troubleshoot', 'help'
        ],
        IntentType.CLARIFICATION: [
            'what', 'how', 'why', 'when', 'where', 'explain', 'clarify',
            'understand', 'mean', 'difference'
        ]
    }
    
    # Complexity indicators
    COMPLEXITY_INDICATORS = {
        ComplexityLevel.SIMPLE: [
            'simple', 'basic', 'easy', 'quick', 'small', 'single'
        ],
        ComplexityLevel.MODERATE: [
            'moderate', 'standard', 'typical', 'normal', 'medium'
        ],
        ComplexityLevel.COMPLEX: [
            'complex', 'advanced', 'sophisticated', 'multiple', 'distributed',
            'scalable', 'high availability', 'multi-region'
        ],
        ComplexityLevel.EXPERT: [
            'enterprise', 'production', 'mission critical', 'fault tolerant',
            'disaster recovery', 'compliance', 'audit', 'governance'
        ]
    }
    
    def __init__(self, vector_search_service=None):
        """
        Initialize semantic reasoning engine
        
        Args:
            vector_search_service: Optional vector search service for embeddings
        """
        self.vector_search_service = vector_search_service
    
    async def analyze_intent(self, user_input: str, context: Optional[Dict[str, Any]] = None) -> SemanticAnalysis:
        """
        Analyze user intent using semantic understanding
        
        Args:
            user_input: User's input text
            context: Optional context from previous interactions
            
        Returns:
            SemanticAnalysis with intent classification and insights
        """
        user_input_lower = user_input.lower()
        
        # Detect primary intent
        primary_intent = self._detect_primary_intent(user_input_lower)
        
        # Detect secondary intents
        secondary_intents = self._detect_secondary_intents(user_input_lower, primary_intent)
        
        # Determine complexity level
        complexity_level = self._determine_complexity(user_input_lower)
        
        # Extract key concepts
        key_concepts = self._extract_key_concepts(user_input)
        
        # Identify implicit requirements
        implicit_requirements = self._identify_implicit_requirements(user_input, key_concepts)
        
        # Detect ambiguities
        ambiguities = self._detect_ambiguities(user_input)
        
        # Calculate confidence
        confidence_score = self._calculate_intent_confidence(
            primary_intent, secondary_intents, key_concepts
        )
        
        # Generate reasoning
        reasoning = self._generate_reasoning(
            primary_intent, secondary_intents, complexity_level, key_concepts
        )
        
        return SemanticAnalysis(
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            complexity_level=complexity_level,
            key_concepts=key_concepts,
            implicit_requirements=implicit_requirements,
            ambiguities=ambiguities,
            confidence_score=confidence_score,
            reasoning=reasoning
        )
    
    def _detect_primary_intent(self, text: str) -> IntentType:
        """Detect primary user intent"""
        intent_scores = {}
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            score = sum(1 for keyword in keywords if keyword in text)
            intent_scores[intent] = score
        
        if not intent_scores or max(intent_scores.values()) == 0:
            return IntentType.UNKNOWN
        
        return max(intent_scores, key=intent_scores.get)
    
    def _detect_secondary_intents(self, text: str, primary_intent: IntentType) -> List[IntentType]:
        """Detect secondary intents"""
        intent_scores = {}
        
        for intent, keywords in self.INTENT_KEYWORDS.items():
            if intent == primary_intent:
                continue
            score = sum(1 for keyword in keywords if keyword in text)
            if score > 0:
                intent_scores[intent] = score
        
        # Return top 2 secondary intents
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        return [intent for intent, score in sorted_intents[:2]]
    
    def _determine_complexity(self, text: str) -> ComplexityLevel:
        """Determine complexity level of request"""
        complexity_scores = {}
        
        for level, indicators in self.COMPLEXITY_INDICATORS.items():
            score = sum(1 for indicator in indicators if indicator in text)
            complexity_scores[level] = score
        
        if not complexity_scores or max(complexity_scores.values()) == 0:
            return ComplexityLevel.MODERATE
        
        return max(complexity_scores, key=complexity_scores.get)
    
    def _extract_key_concepts(self, text: str) -> List[str]:
        """Extract key technical concepts"""
        # AWS services
        aws_services = [
            'lambda', 's3', 'dynamodb', 'ec2', 'rds', 'api gateway',
            'cloudfront', 'cloudwatch', 'iam', 'vpc', 'ecs', 'fargate',
            'sqs', 'sns', 'eventbridge', 'step functions', 'bedrock'
        ]
        
        # Technical concepts
        technical_concepts = [
            'serverless', 'microservices', 'api', 'database', 'storage',
            'compute', 'networking', 'security', 'monitoring', 'logging',
            'authentication', 'authorization', 'encryption', 'scaling'
        ]
        
        concepts = []
        text_lower = text.lower()
        
        for service in aws_services:
            if service in text_lower:
                concepts.append(service.upper() if len(service) <= 3 else service.title())
        
        for concept in technical_concepts:
            if concept in text_lower:
                concepts.append(concept.title())
        
        return list(set(concepts))
    
    def _identify_implicit_requirements(self, text: str, key_concepts: List[str]) -> List[str]:
        """Identify implicit requirements from user input"""
        implicit_reqs = []
        text_lower = text.lower()
        
        # Scalability implications
        if any(word in text_lower for word in ['users', 'traffic', 'load', 'scale']):
            implicit_reqs.append("System must handle variable load and scale automatically")
        
        # Security implications
        if any(word in text_lower for word in ['user', 'account', 'login', 'data']):
            implicit_reqs.append("Security and authentication mechanisms required")
        
        # Cost implications
        if any(word in text_lower for word in ['startup', 'small', 'budget', 'cheap']):
            implicit_reqs.append("Cost optimization is a priority")
        
        # Reliability implications
        if any(word in text_lower for word in ['production', 'business', 'critical', 'important']):
            implicit_reqs.append("High availability and reliability required")
        
        # Monitoring implications
        if any(word in text_lower for word in ['production', 'business', 'users']):
            implicit_reqs.append("Monitoring and alerting should be implemented")
        
        return implicit_reqs
    
    def _detect_ambiguities(self, text: str) -> List[str]:
        """Detect ambiguous or unclear aspects"""
        ambiguities = []
        text_lower = text.lower()
        
        # Vague quantifiers
        vague_terms = ['some', 'few', 'many', 'several', 'lots', 'bunch']
        for term in vague_terms:
            if term in text_lower:
                ambiguities.append(f"Vague quantifier '{term}' - specific numbers needed")
        
        # Missing scale information
        if 'users' in text_lower and not any(num in text for num in ['100', '1000', '10000', 'million']):
            ambiguities.append("Number of users not specified")
        
        # Missing time constraints
        if any(word in text_lower for word in ['process', 'handle', 'compute']) and 'time' not in text_lower:
            ambiguities.append("Performance/latency requirements not specified")
        
        # Missing budget information
        if 'cost' in text_lower and not any(char.isdigit() for char in text):
            ambiguities.append("Specific budget not provided")
        
        return ambiguities
    
    def _calculate_intent_confidence(
        self, 
        primary_intent: IntentType,
        secondary_intents: List[IntentType],
        key_concepts: List[str]
    ) -> float:
        """Calculate confidence in intent detection"""
        base_confidence = 0.5
        
        # Boost for clear primary intent
        if primary_intent != IntentType.UNKNOWN:
            base_confidence += 0.2
        
        # Boost for key concepts
        base_confidence += min(0.2, len(key_concepts) * 0.05)
        
        # Boost for secondary intents
        base_confidence += min(0.1, len(secondary_intents) * 0.05)
        
        return min(1.0, base_confidence)
    
    def _generate_reasoning(
        self,
        primary_intent: IntentType,
        secondary_intents: List[IntentType],
        complexity_level: ComplexityLevel,
        key_concepts: List[str]
    ) -> str:
        """Generate human-readable reasoning"""
        reasoning_parts = []
        
        reasoning_parts.append(f"Primary intent: {primary_intent.value}")
        
        if secondary_intents:
            secondary_str = ", ".join(i.value for i in secondary_intents)
            reasoning_parts.append(f"Secondary intents: {secondary_str}")
        
        reasoning_parts.append(f"Complexity level: {complexity_level.value}")
        
        if key_concepts:
            concepts_str = ", ".join(key_concepts)
            reasoning_parts.append(f"Key concepts: {concepts_str}")
        
        return ". ".join(reasoning_parts)


class GoalAlignmentValidator:
    """Validates that recommendations align with user goals"""
    
    def __init__(self):
        self.semantic_reasoner = SemanticReasoning()
    
    async def validate_alignment(
        self,
        user_goals: List[str],
        recommendation: Dict[str, Any],
        context: Optional[Dict[str, Any]] = None
    ) -> GoalAlignment:
        """
        Validate that recommendation aligns with user goals
        
        Args:
            user_goals: List of user's stated goals
            recommendation: The recommendation to validate
            context: Optional context
            
        Returns:
            GoalAlignment result
        """
        # Extract goals from recommendation
        recommendation_goals = self._extract_recommendation_goals(recommendation)
        
        # Calculate alignment score
        alignment_score = self._calculate_alignment_score(user_goals, recommendation_goals)
        
        # Identify misalignments
        misalignments = self._identify_misalignments(user_goals, recommendation_goals)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(user_goals, recommendation_goals, misalignments)
        
        # Determine if aligned
        is_aligned = alignment_score >= 0.7 and len(misalignments) == 0
        
        return GoalAlignment(
            is_aligned=is_aligned,
            user_goals=user_goals,
            recommendation_goals=recommendation_goals,
            alignment_score=alignment_score,
            misalignments=misalignments,
            suggestions=suggestions
        )
    
    def _extract_recommendation_goals(self, recommendation: Dict[str, Any]) -> List[str]:
        """Extract implicit goals from recommendation"""
        goals = []
        
        # Check for cost optimization
        if 'cost' in str(recommendation).lower():
            goals.append("cost_optimization")
        
        # Check for security
        if 'security' in str(recommendation).lower() or 'iam' in str(recommendation).lower():
            goals.append("security")
        
        # Check for scalability
        if 'scale' in str(recommendation).lower() or 'auto' in str(recommendation).lower():
            goals.append("scalability")
        
        # Check for performance
        if 'performance' in str(recommendation).lower() or 'fast' in str(recommendation).lower():
            goals.append("performance")
        
        return goals
    
    def _calculate_alignment_score(self, user_goals: List[str], rec_goals: List[str]) -> float:
        """Calculate alignment score between goals"""
        if not user_goals:
            return 1.0
        
        # Count matching goals
        user_goals_lower = [g.lower() for g in user_goals]
        rec_goals_lower = [g.lower() for g in rec_goals]
        
        matches = sum(1 for ug in user_goals_lower if any(ug in rg or rg in ug for rg in rec_goals_lower))
        
        return matches / len(user_goals) if user_goals else 0.0
    
    def _identify_misalignments(self, user_goals: List[str], rec_goals: List[str]) -> List[str]:
        """Identify misalignments between goals"""
        misalignments = []
        
        user_goals_lower = [g.lower() for g in user_goals]
        rec_goals_lower = [g.lower() for g in rec_goals]
        
        for ug in user_goals_lower:
            if not any(ug in rg or rg in ug for rg in rec_goals_lower):
                misalignments.append(f"User goal '{ug}' not addressed in recommendation")
        
        return misalignments
    
    def _generate_suggestions(
        self,
        user_goals: List[str],
        rec_goals: List[str],
        misalignments: List[str]
    ) -> List[str]:
        """Generate suggestions for better alignment"""
        suggestions = []
        
        if misalignments:
            suggestions.append("Revise recommendation to address all user goals")
        
        if len(rec_goals) > len(user_goals) * 2:
            suggestions.append("Recommendation may be over-engineered for stated goals")
        
        if not rec_goals:
            suggestions.append("Recommendation should explicitly address user goals")
        
        return suggestions
