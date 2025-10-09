"""
Progressive Disclosure System

Adapts technical depth to user experience level (beginner/intermediate/advanced/expert).
Gradually reveals complexity based on user's demonstrated understanding.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional
from enum import Enum
import logging
import re

logger = logging.getLogger(__name__)


class ExperienceLevel(Enum):
    """User experience levels"""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"


class TechnicalDepth(Enum):
    """Levels of technical detail"""
    BUSINESS_ONLY = "business_only"
    SIMPLIFIED = "simplified"
    STANDARD = "standard"
    DETAILED = "detailed"
    EXPERT = "expert"


@dataclass
class ContentAdaptation:
    """Adapted content for specific experience level"""
    original_content: str
    adapted_content: str
    experience_level: ExperienceLevel
    technical_depth: TechnicalDepth
    additional_resources: List[str]


class ProgressiveDisclosure:
    """
    Adapts content complexity to user's experience level.
    
    Key Features:
    - Detects user experience level from interactions
    - Adapts technical depth appropriately
    - Provides additional resources for learning
    - Gradually increases complexity as user demonstrates understanding
    """
    
    TERM_SIMPLIFICATIONS = {
        'beginner': {
            'Lambda': 'serverless function (code that runs without managing servers)',
            'DynamoDB': 'database (stores your data)',
            'S3': 'file storage (like Dropbox for your application)',
            'API Gateway': 'entry point (how users access your application)',
            'CloudWatch': 'monitoring system (tracks how your application is performing)',
            'IAM': 'security permissions (controls who can access what)',
            'VPC': 'private network (isolated network for your resources)',
            'ECS': 'container service (runs your application in containers)',
            'CloudFormation': 'infrastructure template (defines all your AWS resources)',
            'EventBridge': 'event scheduler (triggers actions at specific times)',
        },
        'intermediate': {
            'Lambda': 'serverless compute service',
            'DynamoDB': 'NoSQL database',
            'S3': 'object storage service',
            'API Gateway': 'managed API service',
            'CloudWatch': 'monitoring and observability service',
            'IAM': 'identity and access management',
            'VPC': 'virtual private cloud',
            'ECS': 'Elastic Container Service',
            'CloudFormation': 'infrastructure as code service',
            'EventBridge': 'serverless event bus',
        }
    }
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.user_experience_history: Dict[str, List[str]] = {}

    def detect_experience_level(
        self,
        user_input: str,
        interaction_history: Optional[List[str]] = None
    ) -> ExperienceLevel:
        """Detect user's experience level from their input."""
        expert_indicators = [
            'vpc', 'subnet', 'cidr', 'iam role', 'lambda layer',
            'cloudformation', 'terraform', 'kubernetes', 'eks',
            'fargate', 'step functions', 'eventbridge', 'kinesis'
        ]
        
        advanced_indicators = [
            'api', 'database', 'lambda', 's3', 'ec2',
            'load balancer', 'auto scaling', 'cloudwatch',
            'docker', 'container', 'microservice'
        ]
        
        intermediate_indicators = [
            'server', 'storage', 'compute', 'cloud',
            'deployment', 'monitoring', 'security'
        ]
        
        input_lower = user_input.lower()
        expert_count = sum(1 for ind in expert_indicators if ind in input_lower)
        advanced_count = sum(1 for ind in advanced_indicators if ind in input_lower)
        intermediate_count = sum(1 for ind in intermediate_indicators if ind in input_lower)
        
        if expert_count >= 3:
            return ExperienceLevel.EXPERT
        elif advanced_count >= 3 or expert_count >= 1:
            return ExperienceLevel.ADVANCED
        elif intermediate_count >= 2 or advanced_count >= 1:
            return ExperienceLevel.INTERMEDIATE
        else:
            return ExperienceLevel.BEGINNER

    def adapt_content(
        self,
        content: str,
        experience_level: ExperienceLevel,
        include_resources: bool = True
    ) -> ContentAdaptation:
        """Adapt content to user's experience level."""
        depth_mapping = {
            ExperienceLevel.BEGINNER: TechnicalDepth.BUSINESS_ONLY,
            ExperienceLevel.INTERMEDIATE: TechnicalDepth.SIMPLIFIED,
            ExperienceLevel.ADVANCED: TechnicalDepth.STANDARD,
            ExperienceLevel.EXPERT: TechnicalDepth.DETAILED
        }
        
        technical_depth = depth_mapping[experience_level]
        adapted = self._apply_simplifications(content, experience_level)
        
        if experience_level == ExperienceLevel.BEGINNER:
            adapted = self._add_beginner_explanations(adapted)
        
        resources = []
        if include_resources and experience_level in [ExperienceLevel.BEGINNER, ExperienceLevel.INTERMEDIATE]:
            resources = self._get_learning_resources(content, experience_level)
        
        return ContentAdaptation(
            original_content=content,
            adapted_content=adapted,
            experience_level=experience_level,
            technical_depth=technical_depth,
            additional_resources=resources
        )

    def _apply_simplifications(self, content: str, experience_level: ExperienceLevel) -> str:
        """Apply term simplifications based on experience level"""
        if experience_level == ExperienceLevel.EXPERT:
            return content
        
        simplified = content
        simplifications = self.TERM_SIMPLIFICATIONS.get(
            experience_level.value,
            self.TERM_SIMPLIFICATIONS.get('intermediate', {})
        )
        
        for term, explanation in simplifications.items():
            pattern = r'\b' + re.escape(term) + r'\b'
            simplified = re.sub(pattern, explanation, simplified, flags=re.IGNORECASE)
        
        return simplified
    
    def _add_beginner_explanations(self, content: str) -> str:
        """Add additional explanations for beginners"""
        if 'AWS' in content and 'Amazon Web Services' not in content:
            content = content.replace('AWS', 'AWS (Amazon Web Services, a cloud computing platform)', 1)
        
        if 'cloud' in content.lower() and 'cloud computing' not in content.lower():
            content = content.replace('cloud', 'cloud (remote servers that run your application)', 1)
        
        return content
    
    def _get_learning_resources(self, content: str, experience_level: ExperienceLevel) -> List[str]:
        """Get relevant learning resources"""
        resources = []
        
        if experience_level == ExperienceLevel.BEGINNER:
            resources.extend([
                "📚 AWS Getting Started Guide: https://aws.amazon.com/getting-started/",
                "📚 What is Cloud Computing?: https://aws.amazon.com/what-is-cloud-computing/",
            ])
        
        if 'Lambda' in content or 'serverless' in content.lower():
            resources.append("📚 AWS Lambda Guide: https://docs.aws.amazon.com/lambda/")
        
        if 'DynamoDB' in content or 'database' in content.lower():
            resources.append("📚 DynamoDB Guide: https://docs.aws.amazon.com/dynamodb/")
        
        return resources
    
    def format_adapted_content(self, adaptation: ContentAdaptation) -> str:
        """Format adapted content for display."""
        output = [adaptation.adapted_content]
        
        if adaptation.additional_resources:
            output.append("\n\n**Learn More:**")
            for resource in adaptation.additional_resources:
                output.append(resource)
        
        return "\n".join(output)
    
    def should_increase_complexity(self, user_id: str, current_level: ExperienceLevel) -> bool:
        """Determine if we should increase complexity for this user."""
        history = self.user_experience_history.get(user_id, [])
        
        if len(history) >= 5:
            recent = history[-5:]
            technical_count = sum(1 for interaction in recent if self._has_technical_terms(interaction))
            if technical_count >= 3:
                return True
        
        return False
    
    def _has_technical_terms(self, text: str) -> bool:

        """Check if text contains technical terms"""
        technical_terms = [
            'lambda', 'dynamodb', 's3', 'api', 'vpc', 'iam',
            'cloudwatch', 'ecs', 'fargate', 'eventbridge'
        ]
        
        text_lower = text.lower()
        return any(term in text_lower for term in technical_terms)
