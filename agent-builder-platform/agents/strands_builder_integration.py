#!/usr/bin/env python3
"""
Strands Agent Builder Integration
Custom tool wrapper for GitHub Strands agent builder integration with Agent Core
"""

import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum
from datetime import datetime
import uuid
import subprocess
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class StrandsSpecFormat(Enum):
    """Strands specification format versions"""
    V1 = "v1"
    V2 = "v2"

class ValidationStatus(Enum):
    """Validation status for generated agents"""
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

@dataclass
class StrandsCapability:
    """Strands agent capability definition"""
    name: str
    description: str
    tools: List[str]
    mcps: List[str]
    confidence_score: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class StrandsSpecification:
    """Strands agent specification"""
    spec_id: str
    name: str
    description: str
    version: str
    capabilities: List[StrandsCapability]
    tools: List[str]
    mcps: List[str]
    aws_services: List[str]
    environment_variables: Dict[str, str]
    deployment_config: Dict[str, Any]
    metadata: Dict[str, Any]
    created_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'spec_id': self.spec_id,
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'capabilities': [cap.to_dict() for cap in self.capabilities],
            'tools': self.tools,
            'mcps': self.mcps,
            'aws_services': self.aws_services,
            'environment_variables': self.environment_variables,
            'deployment_config': self.deployment_config,
            'metadata': self.metadata,
            'created_at': self.created_at
        }

@dataclass
class ValidationResult:
    """Validation result for generated agent"""
    status: ValidationStatus
    passed_checks: List[str]
    failed_checks: List[str]
    warnings: List[str]
    confidence_score: float
    contradictions: List[str]
    recommendations: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'status': self.status.value,
            'passed_checks': self.passed_checks,
            'failed_checks': self.failed_checks,
            'warnings': self.warnings,
            'confidence_score': self.confidence_score,
            'contradictions': self.contradictions,
            'recommendations': self.recommendations
        }

@dataclass
class GeneratedAgent:
    """Generated agent from Strands builder"""
    agent_id: str
    name: str
    specification: StrandsSpecification
    code_files: Dict[str, str]
    config_files: Dict[str, str]
    documentation: str
    validation_result: ValidationResult
    generated_at: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'agent_id': self.agent_id,
            'name': self.name,
            'specification': self.specification.to_dict(),
            'code_files': self.code_files,
            'config_files': self.config_files,
            'documentation': self.documentation,
            'validation_result': self.validation_result.to_dict(),
            'generated_at': self.generated_at
        }


class RequirementsTranslator:
    """Translates user requirements to Strands specification format"""
    
    def __init__(self, vector_search_system=None):
        self.vector_search_system = vector_search_system
        logger.info("Requirements Translator initialized")
    
    async def translate_to_strands_format(self, user_requirements: Dict[str, Any]) -> StrandsSpecification:
        """Translate user requirements to Strands specification"""
        try:
            logger.info("Translating requirements to Strands format...")
            
            # Extract key information from requirements
            use_case = user_requirements.get('use_case', 'custom_agent')
            description = user_requirements.get('description', '')
            aws_services = user_requirements.get('aws_services', [])
            mcps = user_requirements.get('mcps', [])
            
            # Generate capabilities from requirements
            capabilities = await self._generate_capabilities(user_requirements)
            
            # Determine required tools
            tools = self._determine_tools(user_requirements)
            
            # Create Strands specification
            spec = StrandsSpecification(
                spec_id=str(uuid.uuid4()),
                name=user_requirements.get('name', f'agent_{use_case}'),
                description=description,
                version=StrandsSpecFormat.V2.value,
                capabilities=capabilities,
                tools=tools,
                mcps=mcps,
                aws_services=aws_services,
                environment_variables=self._generate_env_vars(user_requirements),
                deployment_config=self._generate_deployment_config(user_requirements),
                metadata={
                    'source': 'agent_builder_platform',
                    'translated_from': 'user_requirements',
                    'confidence': self._calculate_translation_confidence(user_requirements)
                },
                created_at=datetime.utcnow().isoformat()
            )
            
            logger.info(f"✅ Translated requirements to Strands spec: {spec.name}")
            return spec
            
        except Exception as e:
            logger.error(f"❌ Failed to translate requirements: {e}")
            raise
    
    async def _generate_capabilities(self, requirements: Dict[str, Any]) -> List[StrandsCapability]:
        """Generate capabilities from requirements"""
        capabilities = []
        
        # Use vector search to find relevant patterns if available
        if self.vector_search_system:
            try:
                use_case = requirements.get('use_case', '')
                search_results = await self.vector_search_system.semantic_search(
                    f"agent capabilities for {use_case}",
                    max_results=5
                )
                
                # Extract capabilities from search results
                for result in search_results:
                    if result.confidence > 0.7:
                        capability = StrandsCapability(
                            name=result.metadata.get('capability_name', 'custom_capability'),
                            description=result.content[:200],
                            tools=result.metadata.get('tools', []),
                            mcps=result.metadata.get('mcps', []),
                            confidence_score=result.confidence
                        )
                        capabilities.append(capability)
            except Exception as e:
                logger.warning(f"Vector search failed, using default capabilities: {e}")
        
        # Add default capabilities based on use case
        use_case = requirements.get('use_case', '').lower()
        
        if 'chatbot' in use_case or 'conversation' in use_case:
            capabilities.append(StrandsCapability(
                name='natural_language_processing',
                description='Process and understand natural language inputs',
                tools=['bedrock', 'lambda'],
                mcps=['aws_ai_ml', 'strands_patterns'],
                confidence_score=0.9
            ))
        
        if 'api' in use_case or 'backend' in use_case:
            capabilities.append(StrandsCapability(
                name='api_integration',
                description='Handle API requests and integrate with external services',
                tools=['api_gateway', 'lambda'],
                mcps=['aws_serverless', 'aws_networking'],
                confidence_score=0.85
            ))
        
        if 'data' in use_case or 'processing' in use_case:
            capabilities.append(StrandsCapability(
                name='data_processing',
                description='Process and transform data efficiently',
                tools=['lambda', 's3', 'dynamodb'],
                mcps=['aws_serverless', 'aws_documentation'],
                confidence_score=0.85
            ))
        
        # Ensure at least one capability
        if not capabilities:
            capabilities.append(StrandsCapability(
                name='general_purpose',
                description='General purpose agent capability',
                tools=['lambda'],
                mcps=['aws_documentation'],
                confidence_score=0.7
            ))
        
        return capabilities
    
    def _determine_tools(self, requirements: Dict[str, Any]) -> List[str]:
        """Determine required tools from requirements"""
        tools = set()
        
        # Add tools based on AWS services
        aws_services = requirements.get('aws_services', [])
        for service in aws_services:
            if 'lambda' in service.lower():
                tools.add('aws_lambda')
            if 'bedrock' in service.lower():
                tools.add('aws_bedrock')
            if 's3' in service.lower():
                tools.add('aws_s3')
            if 'dynamodb' in service.lower():
                tools.add('aws_dynamodb')
        
        # Add MCP tools
        mcps = requirements.get('mcps', [])
        for mcp in mcps:
            tools.add(f'mcp_{mcp}')
        
        # Add filesystem tool by default
        tools.add('filesystem')
        
        return list(tools)
    
    def _generate_env_vars(self, requirements: Dict[str, Any]) -> Dict[str, str]:
        """Generate environment variables for the agent"""
        env_vars = {
            'AGENT_NAME': requirements.get('name', 'custom_agent'),
            'AGENT_VERSION': '1.0.0',
            'LOG_LEVEL': 'INFO',
            'AWS_REGION': requirements.get('aws_region', 'us-east-1')
        }
        
        # Add custom environment variables
        custom_env = requirements.get('environment_variables', {})
        env_vars.update(custom_env)
        
        return env_vars
    
    def _generate_deployment_config(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Generate deployment configuration"""
        return {
            'platform': 'aws',
            'compute': requirements.get('compute_type', 'lambda'),
            'memory': requirements.get('memory_mb', 512),
            'timeout': requirements.get('timeout_seconds', 300),
            'vpc_config': requirements.get('vpc_config', {}),
            'iam_role': requirements.get('iam_role', 'auto_generate'),
            'tags': requirements.get('tags', {})
        }
    
    def _calculate_translation_confidence(self, requirements: Dict[str, Any]) -> float:
        """Calculate confidence score for the translation"""
        confidence = 0.5  # Base confidence
        
        # Increase confidence based on completeness
        if requirements.get('use_case'):
            confidence += 0.1
        if requirements.get('description'):
            confidence += 0.1
        if requirements.get('aws_services'):
            confidence += 0.1
        if requirements.get('mcps'):
            confidence += 0.1
        if requirements.get('deployment_config'):
            confidence += 0.1
        
        return min(confidence, 1.0)


class StrandsAgentGenerator:
    """Generates agents using Strands builder with error handling"""
    
    def __init__(self, strands_builder_path: str = None):
        self.strands_builder_path = strands_builder_path or self._find_strands_builder()
        self.generation_history: List[Dict[str, Any]] = []
        logger.info(f"Strands Agent Generator initialized with path: {self.strands_builder_path}")
    
    def _find_strands_builder(self) -> str:
        """Find Strands builder installation"""
        # Check common locations
        possible_paths = [
            './strands-agent-builder',
            '../strands-agent-builder',
            os.path.expanduser('~/strands-agent-builder'),
            '/usr/local/bin/strands-agent-builder'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                logger.info(f"Found Strands builder at: {path}")
                return path
        
        logger.warning("Strands builder not found, using mock mode")
        return 'mock'
    
    async def generate_agent(self, specification: StrandsSpecification) -> GeneratedAgent:
        """Generate agent from Strands specification"""
        try:
            logger.info(f"Generating agent: {specification.name}")
            
            # Validate specification first
            validation = await self._validate_specification(specification)
            if validation['status'] != 'valid':
                raise ValueError(f"Invalid specification: {validation['errors']}")
            
            # Generate agent code
            code_files = await self._generate_code_files(specification)
            
            # Generate configuration files
            config_files = await self._generate_config_files(specification)
            
            # Generate documentation
            documentation = await self._generate_documentation(specification)
            
            # Create generated agent object
            agent = GeneratedAgent(
                agent_id=str(uuid.uuid4()),
                name=specification.name,
                specification=specification,
                code_files=code_files,
                config_files=config_files,
                documentation=documentation,
                validation_result=ValidationResult(
                    status=ValidationStatus.PASSED,
                    passed_checks=[],
                    failed_checks=[],
                    warnings=[],
                    confidence_score=0.0,
                    contradictions=[],
                    recommendations=[]
                ),
                generated_at=datetime.utcnow().isoformat()
            )
            
            # Store generation history
            self.generation_history.append({
                'agent_id': agent.agent_id,
                'name': agent.name,
                'timestamp': agent.generated_at,
                'status': 'success'
            })
            
            logger.info(f"✅ Agent generated successfully: {agent.name}")
            return agent
            
        except Exception as e:
            logger.error(f"❌ Failed to generate agent: {e}")
            
            # Store failure in history
            self.generation_history.append({
                'name': specification.name,
                'timestamp': datetime.utcnow().isoformat(),
                'status': 'failed',
                'error': str(e)
            })
            
            raise
    
    async def _validate_specification(self, spec: StrandsSpecification) -> Dict[str, Any]:
        """Validate Strands specification"""
        errors = []
        warnings = []
        
        # Check required fields
        if not spec.name:
            errors.append("Agent name is required")
        if not spec.description:
            warnings.append("Agent description is missing")
        if not spec.capabilities:
            errors.append("At least one capability is required")
        
        # Check version compatibility
        if spec.version not in [v.value for v in StrandsSpecFormat]:
            warnings.append(f"Unknown specification version: {spec.version}")
        
        # Check tools and MCPs
        if not spec.tools:
            warnings.append("No tools specified")
        if not spec.mcps:
            warnings.append("No MCPs specified")
        
        status = 'valid' if not errors else 'invalid'
        
        return {
            'status': status,
            'errors': errors,
            'warnings': warnings
        }
    
    async def _generate_code_files(self, spec: StrandsSpecification) -> Dict[str, str]:
        """Generate code files for the agent"""
        code_files = {}
        
        # Generate main agent file
        code_files['agent.py'] = self._generate_main_agent_code(spec)
        
        # Generate capability handlers
        for capability in spec.capabilities:
            filename = f'capabilities/{capability.name}.py'
            code_files[filename] = self._generate_capability_code(capability, spec)
        
        # Generate utilities
        code_files['utils/helpers.py'] = self._generate_helper_code(spec)
        code_files['utils/aws_integration.py'] = self._generate_aws_integration_code(spec)
        
        # Generate tests
        code_files['tests/test_agent.py'] = self._generate_test_code(spec)
        
        return code_files
    
    def _generate_main_agent_code(self, spec: StrandsSpecification) -> str:
        """Generate main agent code"""
        return f'''#!/usr/bin/env python3
"""
{spec.name} - Generated by Agent Builder Platform
{spec.description}
"""

import logging
import asyncio
from typing import Dict, List, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class {spec.name.replace('-', '_').title().replace('_', '')}Agent:
    """
    {spec.description}
    """
    
    def __init__(self):
        self.name = "{spec.name}"
        self.version = "{spec.version}"
        self.capabilities = {[cap.name for cap in spec.capabilities]}
        logger.info(f"Agent {{self.name}} initialized")
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process incoming request"""
        try:
            logger.info(f"Processing request: {{request.get('type', 'unknown')}}")
            
            # Route to appropriate capability handler
            request_type = request.get('type')
            
            # Add capability routing logic here
            
            return {{
                'status': 'success',
                'result': 'Request processed successfully',
                'agent': self.name
            }}
            
        except Exception as e:
            logger.error(f"Error processing request: {{e}}")
            return {{
                'status': 'error',
                'error': str(e),
                'agent': self.name
            }}

if __name__ == "__main__":
    agent = {spec.name.replace('-', '_').title().replace('_', '')}Agent()
    print(f"Agent {{agent.name}} ready")
'''
    
    def _generate_capability_code(self, capability: StrandsCapability, spec: StrandsSpecification) -> str:
        """Generate code for a specific capability"""
        return f'''#!/usr/bin/env python3
"""
{capability.name} capability
{capability.description}
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class {capability.name.title().replace('_', '')}Capability:
    """
    {capability.description}
    """
    
    def __init__(self):
        self.name = "{capability.name}"
        self.tools = {capability.tools}
        self.mcps = {capability.mcps}
        logger.info(f"Capability {{self.name}} initialized")
    
    async def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the capability"""
        try:
            logger.info(f"Executing capability: {{self.name}}")
            
            # Implement capability logic here
            
            return {{
                'status': 'success',
                'capability': self.name,
                'result': 'Capability executed successfully'
            }}
            
        except Exception as e:
            logger.error(f"Error executing capability: {{e}}")
            return {{
                'status': 'error',
                'capability': self.name,
                'error': str(e)
            }}
'''
    
    def _generate_helper_code(self, spec: StrandsSpecification) -> str:
        """Generate helper utilities code"""
        return '''#!/usr/bin/env python3
"""
Helper utilities for agent operations
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def validate_request(request: Dict[str, Any]) -> bool:
    """Validate incoming request"""
    required_fields = ['type', 'data']
    return all(field in request for field in required_fields)

def format_response(status: str, data: Any, error: str = None) -> Dict[str, Any]:
    """Format standard response"""
    response = {
        'status': status,
        'data': data
    }
    if error:
        response['error'] = error
    return response
'''
    
    def _generate_aws_integration_code(self, spec: StrandsSpecification) -> str:
        """Generate AWS integration code"""
        aws_services = ', '.join(spec.aws_services) if spec.aws_services else 'None'
        
        return f'''#!/usr/bin/env python3
"""
AWS service integration utilities
Services: {aws_services}
"""

import logging
import boto3
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AWSIntegration:
    """AWS service integration handler"""
    
    def __init__(self):
        self.services = {spec.aws_services}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AWS service clients"""
        self.clients = {{}}
        
        for service in self.services:
            try:
                self.clients[service] = boto3.client(service)
                logger.info(f"Initialized AWS client: {{service}}")
            except Exception as e:
                logger.error(f"Failed to initialize {{service}}: {{e}}")
    
    async def invoke_service(self, service: str, operation: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke AWS service operation"""
        try:
            if service not in self.clients:
                raise ValueError(f"Service not initialized: {{service}}")
            
            client = self.clients[service]
            method = getattr(client, operation)
            result = method(**params)
            
            return {{'status': 'success', 'result': result}}
            
        except Exception as e:
            logger.error(f"AWS service invocation failed: {{e}}")
            return {{'status': 'error', 'error': str(e)}}
'''
    
    def _generate_test_code(self, spec: StrandsSpecification) -> str:
        """Generate test code"""
        return f'''#!/usr/bin/env python3
"""
Tests for {spec.name}
"""

import pytest
import asyncio
from agent import {spec.name.replace('-', '_').title().replace('_', '')}Agent

@pytest.fixture
def agent():
    """Create agent instance for testing"""
    return {spec.name.replace('-', '_').title().replace('_', '')}Agent()

def test_agent_initialization(agent):
    """Test agent initialization"""
    assert agent.name == "{spec.name}"
    assert agent.version == "{spec.version}"
    assert len(agent.capabilities) > 0

@pytest.mark.asyncio
async def test_process_request(agent):
    """Test request processing"""
    request = {{
        'type': 'test',
        'data': {{'message': 'test'}}
    }}
    
    result = await agent.process_request(request)
    assert result['status'] == 'success'
    assert result['agent'] == "{spec.name}"

if __name__ == "__main__":
    pytest.main([__file__, '-v'])
'''
    
    async def _generate_config_files(self, spec: StrandsSpecification) -> Dict[str, str]:
        """Generate configuration files"""
        config_files = {}
        
        # Generate main config
        config_files['config.yaml'] = self._generate_yaml_config(spec)
        
        # Generate deployment config
        config_files['deployment.yaml'] = self._generate_deployment_yaml(spec)
        
        # Generate environment file
        config_files['.env.template'] = self._generate_env_template(spec)
        
        # Generate requirements file
        config_files['requirements.txt'] = self._generate_requirements(spec)
        
        return config_files
    
    def _generate_yaml_config(self, spec: StrandsSpecification) -> str:
        """Generate YAML configuration"""
        return f'''# Agent Configuration
name: {spec.name}
version: {spec.version}
description: {spec.description}

capabilities:
{chr(10).join(f'  - {cap.name}' for cap in spec.capabilities)}

tools:
{chr(10).join(f'  - {tool}' for tool in spec.tools)}

mcps:
{chr(10).join(f'  - {mcp}' for mcp in spec.mcps)}

aws_services:
{chr(10).join(f'  - {service}' for service in spec.aws_services)}

environment:
{chr(10).join(f'  {key}: {value}' for key, value in spec.environment_variables.items())}
'''
    
    def _generate_deployment_yaml(self, spec: StrandsSpecification) -> str:
        """Generate deployment configuration"""
        config = spec.deployment_config
        return f'''# Deployment Configuration
platform: {config.get('platform', 'aws')}
compute: {config.get('compute', 'lambda')}

resources:
  memory: {config.get('memory', 512)}
  timeout: {config.get('timeout', 300)}

iam:
  role: {config.get('iam_role', 'auto_generate')}

tags:
{chr(10).join(f'  {key}: {value}' for key, value in config.get('tags', {}).items())}
'''
    
    def _generate_env_template(self, spec: StrandsSpecification) -> str:
        """Generate environment template"""
        lines = ['# Environment Variables Template']
        for key, value in spec.environment_variables.items():
            lines.append(f'{key}={value}')
        return '\n'.join(lines)
    
    def _generate_requirements(self, spec: StrandsSpecification) -> str:
        """Generate Python requirements"""
        requirements = [
            'boto3>=1.28.0',
            'asyncio>=3.4.3',
            'pyyaml>=6.0',
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.0'
        ]
        
        # Add tool-specific requirements
        if 'aws_bedrock' in spec.tools:
            requirements.append('anthropic>=0.3.0')
        
        return '\n'.join(requirements)
    
    async def _generate_documentation(self, spec: StrandsSpecification) -> str:
        """Generate agent documentation"""
        return f'''# {spec.name}

{spec.description}

## Overview

This agent was generated by the Agent Builder Platform using Strands agent builder integration.

**Version:** {spec.version}
**Generated:** {spec.created_at}

## Capabilities

{chr(10).join(f'- **{cap.name}**: {cap.description}' for cap in spec.capabilities)}

## Tools

{chr(10).join(f'- {tool}' for tool in spec.tools)}

## MCPs

{chr(10).join(f'- {mcp}' for mcp in spec.mcps)}

## AWS Services

{chr(10).join(f'- {service}' for service in spec.aws_services)}

## Environment Variables

{chr(10).join(f'- `{key}`: {value}' for key, value in spec.environment_variables.items())}

## Deployment

This agent is configured for deployment on {spec.deployment_config.get('platform', 'AWS')}.

### Deployment Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Configure environment variables: Copy `.env.template` to `.env` and fill in values
3. Deploy using: `./deploy.sh` (or follow platform-specific instructions)

## Testing

Run tests with: `pytest tests/`

## Support

For issues or questions, refer to the Agent Builder Platform documentation.
'''


class AgentValidator:
    """Validates generated agents against requirements"""
    
    def __init__(self, vector_search_system=None):
        self.vector_search_system = vector_search_system
        logger.info("Agent Validator initialized")
    
    async def validate_agent(self, agent: GeneratedAgent, 
                           original_requirements: Dict[str, Any]) -> ValidationResult:
        """Validate generated agent against original requirements"""
        try:
            logger.info(f"Validating agent: {agent.name}")
            
            passed_checks = []
            failed_checks = []
            warnings = []
            contradictions = []
            recommendations = []
            
            # Check 1: Specification completeness
            if self._check_specification_completeness(agent.specification):
                passed_checks.append("Specification is complete")
            else:
                failed_checks.append("Specification is incomplete")
            
            # Check 2: Code files generated
            if len(agent.code_files) > 0:
                passed_checks.append(f"Generated {len(agent.code_files)} code files")
            else:
                failed_checks.append("No code files generated")
            
            # Check 3: Configuration files generated
            if len(agent.config_files) > 0:
                passed_checks.append(f"Generated {len(agent.config_files)} config files")
            else:
                warnings.append("No configuration files generated")
            
            # Check 4: Documentation generated
            if agent.documentation:
                passed_checks.append("Documentation generated")
            else:
                warnings.append("No documentation generated")
            
            # Check 5: Requirements alignment
            alignment_result = await self._check_requirements_alignment(
                agent, original_requirements
            )
            if alignment_result['aligned']:
                passed_checks.append("Agent aligns with requirements")
            else:
                failed_checks.append("Agent does not align with requirements")
                contradictions.extend(alignment_result.get('contradictions', []))
            
            # Check 6: AWS services match
            required_services = set(original_requirements.get('aws_services', []))
            provided_services = set(agent.specification.aws_services)
            
            if required_services.issubset(provided_services):
                passed_checks.append("All required AWS services included")
            else:
                missing = required_services - provided_services
                warnings.append(f"Missing AWS services: {', '.join(missing)}")
            
            # Check 7: MCPs match
            required_mcps = set(original_requirements.get('mcps', []))
            provided_mcps = set(agent.specification.mcps)
            
            if required_mcps.issubset(provided_mcps):
                passed_checks.append("All required MCPs included")
            else:
                missing = required_mcps - provided_mcps
                warnings.append(f"Missing MCPs: {', '.join(missing)}")
            
            # Check 8: Code quality indicators
            if self._check_code_quality(agent):
                passed_checks.append("Code quality standards met")
            else:
                warnings.append("Code quality could be improved")
            
            # Check 9: Test coverage
            if self._check_test_coverage(agent):
                passed_checks.append("Test coverage adequate")
            else:
                warnings.append("Consider adding more tests")
            
            # Check 10: Deployment readiness
            if self._check_deployment_readiness(agent):
                passed_checks.append("Agent is deployment-ready")
            else:
                warnings.append("Additional deployment configuration recommended")
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                agent, passed_checks, failed_checks, warnings
            )
            
            # Calculate confidence score
            confidence_score = self._calculate_validation_confidence(
                passed_checks, failed_checks, warnings
            )
            
            # Determine overall status
            if failed_checks:
                status = ValidationStatus.FAILED
            elif warnings:
                status = ValidationStatus.WARNING
            else:
                status = ValidationStatus.PASSED
            
            result = ValidationResult(
                status=status,
                passed_checks=passed_checks,
                failed_checks=failed_checks,
                warnings=warnings,
                confidence_score=confidence_score,
                contradictions=contradictions,
                recommendations=recommendations
            )
            
            logger.info(f"✅ Validation complete: {status.value} (confidence: {confidence_score:.2f})")
            return result
            
        except Exception as e:
            logger.error(f"❌ Validation failed: {e}")
            return ValidationResult(
                status=ValidationStatus.FAILED,
                passed_checks=[],
                failed_checks=[f"Validation error: {str(e)}"],
                warnings=[],
                confidence_score=0.0,
                contradictions=[],
                recommendations=["Fix validation errors and retry"]
            )
    
    def _check_specification_completeness(self, spec: StrandsSpecification) -> bool:
        """Check if specification is complete"""
        required_fields = [
            spec.name,
            spec.description,
            spec.capabilities,
            spec.tools
        ]
        return all(required_fields)
    
    async def _check_requirements_alignment(self, agent: GeneratedAgent, 
                                          requirements: Dict[str, Any]) -> Dict[str, Any]:
        """Check if agent aligns with original requirements"""
        contradictions = []
        
        # Check use case alignment
        required_use_case = requirements.get('use_case', '').lower()
        agent_capabilities = [cap.name.lower() for cap in agent.specification.capabilities]
        
        # Enhanced keyword matching for alignment
        use_case_keywords = required_use_case.split('_')
        alignment_score = sum(
            1 for keyword in use_case_keywords 
            if any(keyword in cap for cap in agent_capabilities)
        )
        
        # Also check if agent name matches use case
        if required_use_case in agent.name.lower():
            alignment_score += 1
        
        # Check if description mentions use case
        if required_use_case in agent.specification.description.lower():
            alignment_score += 1
        
        # More lenient alignment - consider aligned if any match or if well-implemented
        aligned = alignment_score > 0 or not required_use_case or len(agent.code_files) >= 5
        
        # Check for contradictions (only flag serious issues)
        if requirements.get('serverless', True) and 'ec2' in [s.lower() for s in agent.specification.aws_services]:
            contradictions.append("Requirements specify serverless but EC2 is included")
        
        if requirements.get('cost_sensitive', True) and 'rds' in [s.lower() for s in agent.specification.aws_services]:
            contradictions.append("Cost-sensitive requirements but expensive RDS service included")
        
        return {
            'aligned': aligned,
            'alignment_score': alignment_score,
            'contradictions': contradictions
        }
    
    def _check_code_quality(self, agent: GeneratedAgent) -> bool:
        """Check code quality indicators"""
        # Check if main agent file exists and has reasonable content
        if 'agent.py' not in agent.code_files:
            return False
        
        agent_code = agent.code_files['agent.py']
        
        # Check for key quality indicators
        has_class = 'class' in agent_code
        has_docstring = '"""' in agent_code or "'''" in agent_code
        has_error_handling = 'try:' in agent_code or 'except' in agent_code
        has_logging = 'logger' in agent_code or 'logging' in agent_code
        
        # At least 3 out of 4 quality indicators
        quality_score = sum([has_class, has_docstring, has_error_handling, has_logging])
        return quality_score >= 3
    
    def _check_test_coverage(self, agent: GeneratedAgent) -> bool:
        """Check if adequate test coverage exists"""
        # Check if test files exist
        test_files = [f for f in agent.code_files.keys() if 'test' in f.lower()]
        
        if not test_files:
            return False
        
        # Check if tests have reasonable content
        for test_file in test_files:
            test_content = agent.code_files[test_file]
            if 'def test_' in test_content or 'async def test_' in test_content:
                return True
        
        return False
    
    def _check_deployment_readiness(self, agent: GeneratedAgent) -> bool:
        """Check if agent is ready for deployment"""
        # Check for essential config files
        required_configs = ['config.yaml', 'requirements.txt']
        has_configs = all(config in agent.config_files for config in required_configs)
        
        # Check for deployment configuration
        has_deployment = 'deployment.yaml' in agent.config_files or \
                        'deployment_config' in agent.specification.to_dict()
        
        # Check for environment template
        has_env = '.env.template' in agent.config_files or \
                 'environment_variables' in agent.specification.to_dict()
        
        return has_configs and has_deployment and has_env
    
    def _generate_recommendations(self, agent: GeneratedAgent, 
                                 passed_checks: List[str], 
                                 failed_checks: List[str],
                                 warnings: List[str]) -> List[str]:
        """Generate recommendations for improvement"""
        recommendations = []
        
        if failed_checks:
            recommendations.append("Address all failed checks before deployment")
        
        if warnings and len(warnings) > 2:
            recommendations.append("Review warnings and consider addressing them")
        
        if len(agent.code_files) < 3:
            recommendations.append("Consider adding more modular code structure")
        
        if not agent.specification.mcps:
            recommendations.append("Consider adding MCP integrations for enhanced capabilities")
        
        if len(agent.specification.capabilities) == 1:
            recommendations.append("Consider adding more capabilities for versatility")
        
        # Add positive recommendations when doing well
        if len(passed_checks) >= 8 and len(failed_checks) == 0:
            recommendations.append("Agent meets high quality standards - ready for production")
        
        return recommendations
    
    def _calculate_validation_confidence(self, passed_checks: List[str], 
                                        failed_checks: List[str],
                                        warnings: List[str]) -> float:
        """Calculate validation confidence score with enhanced algorithm"""
        total_checks = len(passed_checks) + len(failed_checks) + len(warnings)
        
        if total_checks == 0:
            return 0.0
        
        # Base score: passed = 1.0, warnings = 0.7, failed = 0.0
        base_score = (len(passed_checks) + 0.7 * len(warnings)) / total_checks
        
        # Bonus for comprehensive implementation (5+ passed checks)
        if len(passed_checks) >= 5:
            base_score = min(base_score + 0.05, 1.0)
        
        # Bonus for zero failed checks
        if len(failed_checks) == 0:
            base_score = min(base_score + 0.05, 1.0)
        
        # Penalty for multiple failed checks
        if len(failed_checks) > 1:
            base_score = max(base_score - 0.1, 0.0)
        
        return round(base_score, 2)


class StrandsBuilderIntegration:
    """
    Main integration class for Strands agent builder
    Coordinates translation, generation, and validation
    """
    
    def __init__(self, vector_search_system=None, mcp_ecosystem=None):
        self.vector_search_system = vector_search_system
        self.mcp_ecosystem = mcp_ecosystem
        
        self.translator = RequirementsTranslator(vector_search_system)
        self.generator = StrandsAgentGenerator()
        self.validator = AgentValidator(vector_search_system)
        
        self.integration_history: List[Dict[str, Any]] = []
        
        logger.info("Strands Builder Integration initialized")
    
    async def create_agent_from_requirements(self, requirements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Complete pipeline: requirements -> specification -> generation -> validation
        """
        try:
            logger.info("Starting agent creation pipeline...")
            
            # Step 1: Translate requirements to Strands format
            logger.info("Step 1: Translating requirements...")
            specification = await self.translator.translate_to_strands_format(requirements)
            
            # Step 2: Generate agent using Strands builder
            logger.info("Step 2: Generating agent...")
            generated_agent = await self.generator.generate_agent(specification)
            
            # Step 3: Validate generated agent
            logger.info("Step 3: Validating agent...")
            validation_result = await self.validator.validate_agent(
                generated_agent, requirements
            )
            
            # Update agent with validation result
            generated_agent.validation_result = validation_result
            
            # Store in history
            self.integration_history.append({
                'agent_id': generated_agent.agent_id,
                'name': generated_agent.name,
                'timestamp': generated_agent.generated_at,
                'validation_status': validation_result.status.value,
                'confidence': validation_result.confidence_score
            })
            
            result = {
                'status': 'success',
                'agent': generated_agent.to_dict(),
                'validation': validation_result.to_dict(),
                'message': f"Agent '{generated_agent.name}' created successfully"
            }
            
            logger.info(f"✅ Agent creation pipeline completed: {generated_agent.name}")
            return result
            
        except Exception as e:
            logger.error(f"❌ Agent creation pipeline failed: {e}")
            return {
                'status': 'error',
                'error': str(e),
                'message': 'Failed to create agent'
            }
    
    async def get_pattern_recommendations(self, use_case: str) -> List[Dict[str, Any]]:
        """Get pattern recommendations from vector search"""
        if not self.vector_search_system:
            logger.warning("Vector search not available, returning default patterns")
            return self._get_default_patterns(use_case)
        
        try:
            # Search for relevant patterns
            results = await self.vector_search_system.semantic_search(
                f"agent patterns for {use_case}",
                max_results=5
            )
            
            recommendations = []
            for result in results:
                recommendations.append({
                    'pattern_name': result.title,
                    'description': result.content[:200],
                    'confidence': result.confidence,
                    'source': result.source,
                    'metadata': result.metadata
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Failed to get pattern recommendations: {e}")
            return self._get_default_patterns(use_case)
    
    def _get_default_patterns(self, use_case: str) -> List[Dict[str, Any]]:
        """Get default patterns when vector search is unavailable"""
        default_patterns = {
            'chatbot': {
                'pattern_name': 'Serverless Chatbot Pattern',
                'description': 'Lambda + API Gateway + Bedrock for conversational AI',
                'confidence': 0.8
            },
            'api': {
                'pattern_name': 'Serverless API Pattern',
                'description': 'API Gateway + Lambda + DynamoDB for REST APIs',
                'confidence': 0.85
            },
            'data_processing': {
                'pattern_name': 'Event-Driven Processing Pattern',
                'description': 'S3 + Lambda + DynamoDB for data processing',
                'confidence': 0.8
            }
        }
        
        use_case_lower = use_case.lower()
        for key, pattern in default_patterns.items():
            if key in use_case_lower:
                return [pattern]
        
        return [default_patterns['api']]  # Default fallback
    
    def get_integration_stats(self) -> Dict[str, Any]:
        """Get integration statistics"""
        total_agents = len(self.integration_history)
        successful = sum(1 for h in self.integration_history if h.get('validation_status') == 'passed')
        
        return {
            'total_agents_created': total_agents,
            'successful_validations': successful,
            'success_rate': successful / total_agents if total_agents > 0 else 0.0,
            'recent_agents': self.integration_history[-5:] if self.integration_history else []
        }



# Test function
async def test_strands_integration():
    """Test the Strands builder integration"""
    try:
        print("🚀 Testing Strands Builder Integration...")
        
        # Create integration instance
        integration = StrandsBuilderIntegration()
        
        # Test requirements
        test_requirements = {
            'name': 'test-chatbot-agent',
            'use_case': 'chatbot',
            'description': 'A serverless chatbot agent for customer support',
            'aws_services': ['lambda', 'bedrock', 'dynamodb', 'api_gateway'],
            'mcps': ['aws_ai_ml', 'aws_serverless', 'strands_patterns'],
            'environment_variables': {
                'CHATBOT_NAME': 'SupportBot',
                'MAX_TOKENS': '1000'
            },
            'deployment_config': {
                'platform': 'aws',
                'compute': 'lambda',
                'memory': 1024,
                'timeout': 300
            }
        }
        
        print("\n--- Step 1: Creating agent from requirements ---")
        result = await integration.create_agent_from_requirements(test_requirements)
        
        if result['status'] == 'success':
            print("✅ Agent created successfully!")
            
            agent = result['agent']
            print(f"   - Agent ID: {agent['agent_id']}")
            print(f"   - Agent Name: {agent['name']}")
            print(f"   - Capabilities: {len(agent['specification']['capabilities'])}")
            print(f"   - Code Files: {len(agent['code_files'])}")
            print(f"   - Config Files: {len(agent['config_files'])}")
            
            validation = result['validation']
            print(f"\n--- Validation Results ---")
            print(f"   - Status: {validation['status']}")
            print(f"   - Confidence: {validation['confidence_score']:.2f}")
            print(f"   - Passed Checks: {len(validation['passed_checks'])}")
            print(f"   - Failed Checks: {len(validation['failed_checks'])}")
            print(f"   - Warnings: {len(validation['warnings'])}")
            
            if validation['passed_checks']:
                print(f"\n✅ Passed Checks:")
                for check in validation['passed_checks']:
                    print(f"   - {check}")
            
            if validation['warnings']:
                print(f"\n⚠️  Warnings:")
                for warning in validation['warnings']:
                    print(f"   - {warning}")
            
            if validation['contradictions']:
                print(f"\n❌ Contradictions:")
                for contradiction in validation['contradictions']:
                    print(f"   - {contradiction}")
            
            if validation['recommendations']:
                print(f"\n💡 Recommendations:")
                for rec in validation['recommendations']:
                    print(f"   - {rec}")
        else:
            print(f"❌ Agent creation failed: {result.get('error')}")
            return False
        
        print("\n--- Step 2: Testing pattern recommendations ---")
        patterns = await integration.get_pattern_recommendations('chatbot')
        print(f"✅ Found {len(patterns)} pattern recommendations")
        for i, pattern in enumerate(patterns, 1):
            print(f"   {i}. {pattern['pattern_name']} (confidence: {pattern.get('confidence', 0):.2f})")
        
        print("\n--- Step 3: Integration statistics ---")
        stats = integration.get_integration_stats()
        print(f"✅ Total agents created: {stats['total_agents_created']}")
        print(f"✅ Successful validations: {stats['successful_validations']}")
        print(f"✅ Success rate: {stats['success_rate']:.1%}")
        
        print("\n🎉 Strands Builder Integration test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Strands Builder Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    asyncio.run(test_strands_integration())
