#!/usr/bin/env python3
"""
Dependency Injection for FastAPI
Provides orchestrator and service instances
"""

import sys
import os
from typing import Optional

# Add agents directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-core'))

from aws_solutions_architect import AWSolutionsArchitect
from architecture_advisor import ArchitectureAdvisor
from implementation_guide import ImplementationGuideAgent
from testing_validator import TestingValidator
from strands_builder_integration import StrandsBuilderIntegration

# Global agent instances (singleton pattern)
_aws_architect: Optional[AWSolutionsArchitect] = None
_architecture_advisor: Optional[ArchitectureAdvisor] = None
_implementation_guide: Optional[ImplementationGuideAgent] = None
_testing_validator: Optional[TestingValidator] = None
_strands_builder: Optional[StrandsBuilderIntegration] = None

def get_aws_architect() -> AWSolutionsArchitect:
    """Get AWS Solutions Architect agent instance"""
    global _aws_architect
    if _aws_architect is None:
        _aws_architect = AWSolutionsArchitect()
    return _aws_architect

def get_architecture_advisor() -> ArchitectureAdvisor:
    """Get Architecture Advisor agent instance"""
    global _architecture_advisor
    if _architecture_advisor is None:
        _architecture_advisor = ArchitectureAdvisor()
    return _architecture_advisor

def get_implementation_guide() -> ImplementationGuideAgent:
    """Get Implementation Guide agent instance"""
    global _implementation_guide
    if _implementation_guide is None:
        _implementation_guide = ImplementationGuideAgent()
    return _implementation_guide

def get_testing_validator() -> TestingValidator:
    """Get Testing Validator agent instance"""
    global _testing_validator
    if _testing_validator is None:
        _testing_validator = TestingValidator()
    return _testing_validator

def get_strands_builder() -> StrandsBuilderIntegration:
    """Get Strands Builder Integration agent instance"""
    global _strands_builder
    if _strands_builder is None:
        _strands_builder = StrandsBuilderIntegration()
    return _strands_builder
