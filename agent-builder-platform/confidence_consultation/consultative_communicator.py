"""
Consultative Communication System

Converts directive language to collaborative patterns and formats responses
in a consultative manner that makes users feel consulted and confident.
"""

from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
import re
import logging

logger = logging.getLogger(__name__)


class CommunicationPattern(Enum):
    """Communication pattern transformations"""
    DIRECTIVE_TO_COLLABORATIVE = "directive_to_collaborative"
    TECHNICAL_TO_BUSINESS = "technical_to_business"
    PRESCRIPTIVE_TO_OPTIONS = "prescriptive_to_options"


@dataclass
class ResponseFormat:
    """Structured format for consultative responses"""
    introduction: str
    main_content: str
    reasoning: List[str]
    alternatives: List[Dict[str, str]]
    confidence_statement: str
    check_in_question: str


class ConsultativeCommunicator:
    """
    Transforms agent responses into consultative communication patterns.
    
    Key Transformations:
    - "You must..." → "I recommend..."
    - "Do this..." → "Let's explore..."
    - "The only way..." → "The best approach..."
    - Adds reasoning and alternatives
    - Includes confidence transparency
    - Ends with check-in questions
    """
    
    # Directive to collaborative patterns
    DIRECTIVE_PATTERNS = [
        (r'\bYou must\b', 'I recommend'),
        (r'\bYou should\b', 'I suggest'),
        (r'\bYou need to\b', 'It would be beneficial to'),
        (r'\bDo this\b', 'What if we'),
        (r'\bDon\'t do\b', 'I\'d advise against'),
        (r'\bThe only way is\b', 'The best approach is'),
        (r'\bThis is wrong\b', 'I see a potential issue here'),
        (r'\bObviously\b', 'Based on AWS best practices'),
        (r'\bJust use\b', 'I suggest using'),
        (r'\bSimply\b', 'We can'),
        (r'\bNever\b', 'I recommend avoiding'),
        (r'\bAlways\b', 'In most cases'),
    ]
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def make_consultative(self, content: str) -> str:
        """
        Convert directive language to consultative patterns.
        
        Args:
            content: Original content with directive language
            
        Returns:
            Content with collaborative language
        """
        consultative = content
        
        for pattern, replacement in self.DIRECTIVE_PATTERNS:
            consultative = re.sub(pattern, replacement, consultative, flags=re.IGNORECASE)
        
        return consultative
    
    def format_consultative_response(
        self,
        recommendation: Dict[str, Any],
        confidence_score: Any,
        alternatives: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Format response with consultative structure.
        
        Args:
            recommendation: Main recommendation content
            confidence_score: EnhancedConfidenceScore object
            alternatives: Optional alternative approaches
            
        Returns:
            Formatted consultative response
        """
        # Make content consultative
        main_content = self.make_consultative(
            recommendation.get('content', recommendation.get('description', ''))
        )
        
        # Build response
        output = [
            "Based on your requirements, let's explore this approach:\n",
            main_content,
            ""
        ]
        
        # Add confidence transparency
        if confidence_score:
            confidence_pct = int(confidence_score.overall_confidence * 100)
            output.append(f"\n**Why I'm confident ({confidence_pct}%):**")
            for booster in confidence_score.confidence_boosters:
                output.append(f"  ✓ {booster}")
        
        # Add uncertainties if any
        if confidence_score and confidence_score.uncertainty_factors:
            output.append("\n**What I'm assuming:**")
            for uncertainty in confidence_score.uncertainty_factors:
                output.append(f"  ⚠️  {uncertainty}")
        
        # Add alternatives
        if alternatives:
            output.append("\n**Alternative approaches to consider:**")
            for i, alt in enumerate(alternatives, 1):
                output.append(f"\n{i}. {alt.get('name', 'Alternative')}")
                output.append(f"   Pros: {alt.get('pros', 'N/A')}")
                output.append(f"   Cons: {alt.get('cons', 'N/A')}")
                if alt.get('recommendation'):
                    output.append(f"   → {alt['recommendation']}")
        
        # Add check-in question
        output.append("\n" + self._get_check_in_question(recommendation))
        
        return "\n".join(output)
    
    def _get_check_in_question(self, recommendation: Dict[str, Any]) -> str:
        """Generate appropriate check-in question"""
        phase = recommendation.get('phase', 'general')
        
        questions = {
            'requirements': "Does this align with your vision? Would you like me to explore any alternatives or adjust this approach?",
            'architecture': "Does this architecture design meet your needs? Should we explore different service combinations?",
            'implementation': "Does this implementation approach work for you? Would you like me to adjust any technical details?",
            'testing': "Are you comfortable with this testing strategy? Should we add more validation steps?",
            'general': "Does this align with what you're looking for? Would you like me to explore alternatives?"
        }
        
        return questions.get(phase, questions['general'])
    
    def present_options(
        self,
        options: List[Dict[str, Any]],
        context: str = ""
    ) -> str:
        """
        Present 2-3 options with clear trade-offs.
        
        Args:
            options: List of options to present (2-3 recommended)
            context: Context for the options
            
        Returns:
            Formatted options presentation
        """
        output = []
        
        if context:
            output.append(f"{context}\n")
        
        output.append("I see a few approaches we could take:\n")
        
        for i, option in enumerate(options[:3], 1):  # Limit to 3 options
            output.append(f"\n**Option {i}: {option.get('name', 'Approach')}**")
            output.append(f"{option.get('description', '')}")
            
            if option.get('pros'):
                output.append("\nPros:")
                for pro in option['pros'] if isinstance(option['pros'], list) else [option['pros']]:
                    output.append(f"  ✓ {pro}")
            
            if option.get('cons'):
                output.append("\nCons:")
                for con in option['cons'] if isinstance(option['cons'], list) else [option['cons']]:
                    output.append(f"  ✗ {con}")
            
            if option.get('best_for'):
                output.append(f"\nBest for: {option['best_for']}")
            
            if option.get('recommended') and option['recommended']:
                output.append("\n⭐ **Recommended** - This is typically the best approach for your use case")
        
        output.append("\n\nWhich approach resonates with you? Or would you like me to explain any of these in more detail?")
        
        return "\n".join(output)
    
    def add_certainty_indicators(self, content: str, certainty_level: str) -> str:
        """
        Add certainty indicators to language.
        
        Args:
            content: Original content
            certainty_level: 'high', 'medium', or 'low'
            
        Returns:
            Content with certainty indicators
        """
        indicators = {
            'high': [
                "I'm certain that",
                "Based on AWS best practices",
                "This is a proven pattern",
                "Industry standard approach"
            ],
            'medium': [
                "In most cases",
                "Typically",
                "Generally speaking",
                "Based on common patterns"
            ],
            'low': [
                "One possible approach is",
                "We could consider",
                "This might work if",
                "Depending on your specific needs"
            ]
        }
        
        indicator = indicators.get(certainty_level, indicators['medium'])[0]
        
        # Add indicator at the beginning if not already present
        if not any(ind.lower() in content.lower() for ind in indicators.get(certainty_level, [])):
            return f"{indicator}, {content[0].lower()}{content[1:]}"
        
        return content
    
    def format_reasoning(self, reasoning_steps: List[str]) -> str:
        """
        Format reasoning steps for transparency.
        
        Args:
            reasoning_steps: List of reasoning steps
            
        Returns:
            Formatted reasoning explanation
        """
        output = ["\n**My reasoning:**\n"]
        
        for i, step in enumerate(reasoning_steps, 1):
            output.append(f"{i}. {step}")
        
        return "\n".join(output)