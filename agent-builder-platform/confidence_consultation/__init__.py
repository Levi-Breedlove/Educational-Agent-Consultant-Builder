"""
Enhanced Confidence Scoring and Consultative Communication System

This module implements the 95% confidence baseline enforcement and consultative
communication patterns to ensure users feel confident and consulted throughout
the agent creation process.

Key Components:
- EnhancedConfidenceScore: Multi-factor weighted confidence scoring
- UncertaintyAnalysis: Tracking known-knowns, known-unknowns, assumed-knowns
- MultiSourceValidator: Cross-validation across MCPs, vector search, WAF, cost models
- ConsultativeCommunicator: Converting directive to collaborative language
- ActiveListeningService: Validation loops and understanding confirmation
- ProgressiveDisclosure: Adapting technical depth to user experience
- ConfidenceMonitor: Dashboard tracking confidence metrics
"""

from .confidence_scoring import (
    EnhancedConfidenceScore,
    ConfidenceCalculationService,
    ConfidenceFactor
)

from .uncertainty_analysis import (
    UncertaintyAnalysis,
    UncertaintyTracker,
    KnowledgeType
)

from .multi_source_validator import (
    MultiSourceValidator,
    ValidationSource,
    ValidationResult
)

from .consultative_communicator import (
    ConsultativeCommunicator,
    CommunicationPattern,
    ResponseFormat
)

from .active_listening import (
    ActiveListeningService,
    UnderstandingValidation,
    CheckInPrompt,
    CheckInPhase
)

from .progressive_disclosure import (
    ProgressiveDisclosure,
    ExperienceLevel,
    TechnicalDepth,
    ContentAdaptation
)

from .confidence_monitor import (
    ConfidenceMonitor,
    ConfidenceMetrics,
    MonitoringDashboard,
    ConfidenceStatus
)

__all__ = [
    # Confidence Scoring
    'EnhancedConfidenceScore',
    'ConfidenceCalculationService',
    'ConfidenceFactor',
    
    # Uncertainty Analysis
    'UncertaintyAnalysis',
    'UncertaintyTracker',
    'KnowledgeType',
    
    # Multi-Source Validation
    'MultiSourceValidator',
    'ValidationSource',
    'ValidationResult',
    
    # Consultative Communication
    'ConsultativeCommunicator',
    'CommunicationPattern',
    'ResponseFormat',
    
    # Active Listening
    'ActiveListeningService',
    'UnderstandingValidation',
    'CheckInPrompt',
    'CheckInPhase',
    
    # Progressive Disclosure
    'ProgressiveDisclosure',
    'ExperienceLevel',
    'TechnicalDepth',
    'ContentAdaptation',
    
    # Monitoring
    'ConfidenceMonitor',
    'ConfidenceMetrics',
    'MonitoringDashboard',
    'ConfidenceStatus'
]
