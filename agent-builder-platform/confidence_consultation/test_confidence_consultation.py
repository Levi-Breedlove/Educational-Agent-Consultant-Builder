"""
Test Suite for Enhanced Confidence Scoring and Consultative Communication

Tests all components of the confidence consultation system.
"""

import asyncio
from confidence_scoring import (
    EnhancedConfidenceScore,
    ConfidenceCalculationService,
    ConfidenceFactor
)
from uncertainty_analysis import (
    UncertaintyAnalysis,
    UncertaintyTracker,
    KnowledgeType
)
from multi_source_validator import (
    MultiSourceValidator,
    ValidationSource
)
from consultative_communicator import (
    ConsultativeCommunicator,
    ResponseFormat
)
from active_listening import (
    ActiveListeningService,
    CheckInPhase
)
from progressive_disclosure import (
    ProgressiveDisclosure,
    ExperienceLevel
)
from confidence_monitor import (
    MonitoringDashboard,
    ConfidenceStatus
)


def test_confidence_scoring():
    """Test enhanced confidence scoring"""
    print("\n" + "="*60)
    print("TEST: Enhanced Confidence Scoring")
    print("="*60)
    
    # Create a sample analysis
    analysis = {
        'user_goals': ['Build a serverless API'],
        'requirements': [
            {'description': 'RESTful API with authentication'},
            {'description': 'DynamoDB for data storage', 'acceptance_criteria': ['CRUD operations']}
        ],
        'constraints': ['Budget: $50/month'],
        'success_criteria': ['99.9% uptime'],
        'aws_services': ['Lambda', 'API Gateway', 'DynamoDB'],
        'architecture_pattern': 'Serverless',
        'validated_assumptions': True,
        'mcp_validation': True,
        'cost_validation': True
    }
    
    # Calculate confidence
    service = ConfidenceCalculationService()
    score = asyncio.run(service.calculate_confidence(analysis, phase='architecture'))
    
    print(f"\nConfidence Score: {int(score.overall_confidence * 100)}%")
    print(f"Meets Baseline: {score.meets_baseline()}")
    print(f"\nBreakdown:")
    for factor, value in score.get_confidence_breakdown().items():
        print(f"  {factor}: {int(value * 100)}%")
    
    print(f"\nBoosters: {len(score.confidence_boosters)}")
    for booster in score.confidence_boosters:
        print(f"  + {booster}")
    
    print("\n✅ Confidence scoring test passed")
    return score


def test_uncertainty_analysis():
    """Test uncertainty tracking"""
    print("\n" + "="*60)
    print("TEST: Uncertainty Analysis")
    print("="*60)
    
    # Create uncertainty analysis
    uncertainty = UncertaintyAnalysis()
    
    # Add known knowns
    uncertainty.known_knowns.extend([
        "User wants serverless architecture",
        "Budget is $50/month",
        "DynamoDB for storage"
    ])
    
    # Add known unknowns
    uncertainty.known_unknowns.extend([
        "Expected user load not specified",
        "Data volume requirements unclear"
    ])
    
    # Add assumptions
    uncertainty.assumed_knowns.extend([
        "Assuming 1000 users/day",
        "Assuming us-east-1 region"
    ])
    
    # Calculate penalty
    penalty = uncertainty.calculate_confidence_penalty()
    
    print(f"\nConfidence Penalty: -{int(penalty * 100)}%")
    print(f"Known Knowns: {len(uncertainty.known_knowns)}")
    print(f"Known Unknowns: {len(uncertainty.known_unknowns)} (3% each)")
    print(f"Assumptions: {len(uncertainty.assumed_knowns)} (2% each)")
    
    print("\n✅ Uncertainty analysis test passed")
    return uncertainty


def test_multi_source_validation():
    """Test multi-source validation"""
    print("\n" + "="*60)
    print("TEST: Multi-Source Validation")
    print("="*60)
    
    # Create validator
    validator = MultiSourceValidator()
    
    # Create recommendation
    recommendation = {
        'aws_services': ['Lambda', 'DynamoDB', 'API Gateway'],
        'architecture_pattern': 'Serverless REST API',
        'security_controls': ['IAM', 'API Keys'],
        'cost_estimate': '$45/month',
        'within_budget': True,
        'cost_optimization': ['Reserved capacity', 'Auto-scaling']
    }
    
    # Validate
    confidence = asyncio.run(validator.validate_recommendation(recommendation))
    
    print(f"\nValidation Confidence: {int(confidence * 100)}%")
    print(f"Boost Applied: {confidence >= 0.95}")
    
    print("\n✅ Multi-source validation test passed")
    return confidence


def test_consultative_communication():
    """Test consultative communication"""
    print("\n" + "="*60)
    print("TEST: Consultative Communication")
    print("="*60)
    
    communicator = ConsultativeCommunicator()
    
    # Test directive to collaborative
    directive = "You must use Lambda for this. You should implement API Gateway. Never use EC2."
    consultative = communicator.make_consultative(directive)
    
    print("\nOriginal (Directive):")
    print(f"  {directive}")
    print("\nTransformed (Consultative):")
    print(f"  {consultative}")
    
    # Test options presentation
    options = [
        {
            'name': 'Serverless Architecture',
            'description': 'Use Lambda + API Gateway + DynamoDB',
            'pros': ['Cost-effective', 'Auto-scaling', 'No server management'],
            'cons': ['Cold starts', 'Vendor lock-in'],
            'best_for': 'Variable workloads',
            'recommended': True
        },
        {
            'name': 'Container-based',
            'description': 'Use ECS Fargate + RDS',
            'pros': ['Consistent performance', 'More control'],
            'cons': ['Higher cost', 'More management'],
            'best_for': 'Predictable workloads'
        }
    ]
    
    presentation = communicator.present_options(options, "For your API, I see two main approaches:")
    print("\n" + presentation[:200] + "...")
    
    print("\n✅ Consultative communication test passed")


def test_active_listening():
    """Test active listening"""
    print("\n" + "="*60)
    print("TEST: Active Listening")
    print("="*60)
    
    service = ActiveListeningService()
    
    # Test understanding summary
    interpretation = {
        'description': 'Build a serverless REST API for user management',
        'requirements': [
            'User authentication',
            'CRUD operations',
            'Email notifications'
        ],
        'constraints': ['Budget: $50/month', 'Timeline: 2 weeks'],
        'goals': ['Learn serverless', 'Deploy to production']
    }
    
    summary = service._generate_understanding_summary(interpretation)
    print("\n" + summary[:300] + "...")
    
    # Test check-in generation
    output = {
        'architecture_pattern': 'Serverless',
        'aws_services': ['Lambda', 'API Gateway', 'DynamoDB'],
        'cost_estimate': '$45/month'
    }
    
    check_in = service.generate_check_in(CheckInPhase.ARCHITECTURE, output)
    formatted = service.format_check_in(check_in)
    print("\n" + formatted[:200] + "...")
    
    print("\n✅ Active listening test passed")


def test_progressive_disclosure():
    """Test progressive disclosure"""
    print("\n" + "="*60)
    print("TEST: Progressive Disclosure")
    print("="*60)
    
    disclosure = ProgressiveDisclosure()
    
    # Test experience level detection
    beginner_input = "I want to build a website that stores user data"
    expert_input = "I need a Lambda function with VPC integration and custom IAM roles"
    
    beginner_level = disclosure.detect_experience_level(beginner_input)
    expert_level = disclosure.detect_experience_level(expert_input)
    
    print(f"\nBeginner Input: '{beginner_input}'")
    print(f"Detected Level: {beginner_level.value}")
    
    print(f"\nExpert Input: '{expert_input}'")
    print(f"Detected Level: {expert_level.value}")
    
    # Test content adaptation
    technical_content = "We'll use Lambda with DynamoDB and S3 for storage"
    
    beginner_adaptation = disclosure.adapt_content(technical_content, ExperienceLevel.BEGINNER)
    print(f"\nOriginal: {technical_content}")
    print(f"Adapted for Beginner: {beginner_adaptation.adapted_content[:100]}...")
    
    print("\n✅ Progressive disclosure test passed")


def test_confidence_monitoring():
    """Test confidence monitoring"""
    print("\n" + "="*60)
    print("TEST: Confidence Monitoring")
    print("="*60)
    
    dashboard = MonitoringDashboard()
    session_id = "test-session-001"
    
    # Track confidence through phases
    phases = [
        ('requirements', 0.92),
        ('architecture', 0.96),
        ('implementation', 0.94),
        ('testing', 0.97)
    ]
    
    for phase, confidence in phases:
        metrics = dashboard.track_confidence(session_id, phase, confidence)
        print(f"\n{phase.capitalize()}: {int(confidence * 100)}% (trend: {metrics.confidence_trend})")
        if metrics.alerts:
            for alert in metrics.alerts:
                print(f"  {alert}")
    
    # Record user feedback
    dashboard.record_user_feedback(session_id, 0.95, "Great experience!")
    
    # Get summary
    summary = dashboard.get_session_summary(session_id)
    print(f"\nSession Summary:")
    print(f"  Average Confidence: {int(summary['confidence']['average'] * 100)}%")
    print(f"  Status: {summary['status']}")
    print(f"  User Satisfaction: {int(summary['user_satisfaction']['average'] * 100)}%")
    
    print("\n✅ Confidence monitoring test passed")


def test_integration():
    """Test integrated workflow"""
    print("\n" + "="*60)
    print("TEST: Integrated Workflow")
    print("="*60)
    
    # Simulate a complete workflow
    session_id = "integration-test-001"
    
    # 1. Detect experience level
    disclosure = ProgressiveDisclosure()
    user_input = "I want to build a REST API with user authentication"
    experience_level = disclosure.detect_experience_level(user_input)
    print(f"\n1. Experience Level: {experience_level.value}")
    
    # 2. Calculate confidence
    analysis = {
        'user_goals': ['Build REST API'],
        'requirements': [{'description': 'User authentication'}],
        'aws_services': ['Lambda', 'API Gateway'],
        'validated_assumptions': True
    }
    
    service = ConfidenceCalculationService()
    score = asyncio.run(service.calculate_confidence(analysis))
    print(f"2. Confidence Score: {int(score.overall_confidence * 100)}%")
    
    # 3. Track uncertainty
    tracker = UncertaintyTracker()
    uncertainty = asyncio.run(tracker.track_uncertainties('requirements', analysis))
    penalty = uncertainty.calculate_confidence_penalty()
    print(f"3. Uncertainty Penalty: -{int(penalty * 100)}%")
    
    # 4. Apply consultative communication
    communicator = ConsultativeCommunicator()
    recommendation = {
        'content': 'You must use Lambda and API Gateway for this',
        'phase': 'architecture'
    }
    consultative_response = communicator.make_consultative(recommendation['content'])
    print(f"4. Consultative Response: {consultative_response[:60]}...")
    
    # 5. Monitor confidence
    dashboard = MonitoringDashboard()
    metrics = dashboard.track_confidence(session_id, 'requirements', score.overall_confidence)
    print(f"5. Monitoring Status: {dashboard.get_status(metrics.current_confidence).value}")
    
    print("\n✅ Integration test passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("ENHANCED CONFIDENCE & CONSULTATION TEST SUITE")
    print("="*60)
    
    try:
        test_confidence_scoring()
        test_uncertainty_analysis()
        test_multi_source_validation()
        test_consultative_communication()
        test_active_listening()
        test_progressive_disclosure()
        test_confidence_monitoring()
        test_integration()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
