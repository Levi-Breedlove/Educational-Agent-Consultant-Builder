#!/usr/bin/env python3
"""
Export and Deployment Service
Manages agent export in multiple formats and deployment script generation
"""

import logging
import sys
import os
import json
import zipfile
import io
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

# Add paths for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agent-core'))

try:
    from implementation_guide import ImplementationGuideAgent
    from strands_builder_integration import StrandsBuilderIntegration
except ImportError as e:
    logging.warning(f"Could not import agents: {e}")
    class ImplementationGuideAgent:
        async def generate_implementation(self, **kwargs):
            return type('obj', (object,), {'__dict__': {}})()
    class StrandsBuilderIntegration:
        async def generate_strands_agent(self, **kwargs):
            return type('obj', (object,), {'to_dict': lambda: {}})()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ExportFormat(str, Enum):
    """Export format types"""
    CODE = "code"
    IAC = "iac"
    CONTAINER = "container"
    STRANDS = "strands"
    COMPLETE = "complete"


class DeploymentTarget(str, Enum):
    """Deployment target platforms"""
    AWS_LAMBDA = "aws_lambda"
    AWS_ECS = "aws_ecs"
    AWS_FARGATE = "aws_fargate"
    LOCAL = "local"
    DOCKER = "docker"


class ExportService:
    """Service for exporting and deploying agents"""
    
    def __init__(self):
        """Initialize export service"""
        self.implementation_guide = ImplementationGuideAgent()
        self.strands_builder = StrandsBuilderIntegration()
        logger.info("Export service initialized")
    
    async def export_agent(
        self,
        agent_id: str,
        workflow_data: Dict[str, Any],
        export_format: ExportFormat = ExportFormat.COMPLETE,
        include_tests: bool = True
    ) -> Dict[str, Any]:
        """Export agent in specified format"""
        try:
            logger.info(f"Exporting agent {agent_id} in format: {export_format.value}")
            
            requirements = workflow_data.get('requirements', {})
            architecture = workflow_data.get('architecture', {})
            implementation = workflow_data.get('implementation', {})
            
            export_package = {
                'agent_id': agent_id,
                'export_format': export_format.value,
                'exported_at': datetime.utcnow().isoformat(),
                'files': {},
                'metadata': {},
                'deployment_instructions': []
            }
            
            # Generate files based on export format
            if export_format in [ExportFormat.CODE, ExportFormat.COMPLETE]:
                code_files = await self._generate_code_files(requirements, architecture, implementation, include_tests)
                export_package['files'].update(code_files)
            
            if export_format in [ExportFormat.IAC, ExportFormat.COMPLETE]:
                iac_files = await self._generate_iac_files(requirements, architecture)
                export_package['files'].update(iac_files)
            
            if export_format in [ExportFormat.CONTAINER, ExportFormat.COMPLETE]:
                container_files = await self._generate_container_files(requirements, architecture)
                export_package['files'].update(container_files)
            
            if export_format in [ExportFormat.STRANDS, ExportFormat.COMPLETE]:
                strands_files = await self._generate_strands_files(requirements, architecture, implementation)
                export_package['files'].update(strands_files)
            
            # Always include documentation
            doc_files = await self._generate_documentation(requirements, architecture, implementation)
            export_package['files'].update(doc_files)
            
            # Generate deployment instructions
            export_package['deployment_instructions'] = await self._generate_deployment_instructions(
                requirements, architecture, export_format
            )
            
            # Update metadata
            export_package['metadata'] = {
                'agent_name': requirements.get('use_case', 'custom_agent'),
                'description': requirements.get('description', ''),
                'file_count': len(export_package['files']),
                'export_size_bytes': sum(len(str(c)) for c in export_package['files'].values()),
                'aws_services': architecture.get('aws_services', []),
                'mcps': architecture.get('mcps', []),
                'estimated_cost': architecture.get('cost_estimate', 'Unknown'),
                'includes_tests': include_tests
            }
            
            logger.info(f"✅ Agent exported: {len(export_package['files'])} files")
            return export_package
            
        except Exception as e:
            logger.error(f"❌ Export failed: {e}")
            raise
    
    async def _generate_code_files(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any],
        implementation: Dict[str, Any],
        include_tests: bool
    ) -> Dict[str, str]:
        """Generate code files"""
        files = {}
        
        use_case = requirements.get('use_case', 'custom_agent')
        aws_services = architecture.get('aws_services', [])
        
        # Main application file
        files['src/agent.py'] = self._generate_main_agent_code(use_case, requirements, architecture)
        
        # Configuration file
        files['src/config.py'] = self._generate_config_code(requirements, architecture)
        
        # AWS integration utilities
        if aws_services:
            files['src/aws_integration.py'] = self._generate_aws_integration_code(aws_services)
        
        # MCP integration
        mcps = architecture.get('mcps', [])
        if mcps:
            files['src/mcp_integration.py'] = self._generate_mcp_integration_code(mcps)
        
        # Helper utilities
        files['src/utils.py'] = self._generate_utils_code()
        
        # Requirements file
        files['requirements.txt'] = self._generate_requirements_txt(aws_services, mcps)
        
        # Environment template
        files['.env.template'] = self._generate_env_template(requirements, architecture)
        
        # Tests
        if include_tests:
            files['tests/test_agent.py'] = self._generate_test_code(use_case)
            files['tests/test_integration.py'] = self._generate_integration_test_code(use_case, aws_services)
        
        return files
    
    async def _generate_iac_files(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate Infrastructure as Code files"""
        files = {}
        
        # CloudFormation template
        files['infrastructure/cloudformation-template.yaml'] = self._generate_cloudformation_template(
            requirements, architecture
        )
        
        # Terraform configuration (alternative)
        files['infrastructure/terraform/main.tf'] = self._generate_terraform_main(requirements, architecture)
        files['infrastructure/terraform/variables.tf'] = self._generate_terraform_variables()
        files['infrastructure/terraform/outputs.tf'] = self._generate_terraform_outputs()
        
        # Deployment scripts
        files['infrastructure/deploy.sh'] = self._generate_deploy_script()
        files['infrastructure/teardown.sh'] = self._generate_teardown_script()
        
        return files
    
    async def _generate_container_files(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate container files"""
        files = {}
        
        # Dockerfile
        files['Dockerfile'] = self._generate_dockerfile(requirements, architecture)
        
        # Docker Compose
        files['docker-compose.yml'] = self._generate_docker_compose(requirements)
        
        # Docker build script
        files['scripts/build-docker.sh'] = self._generate_docker_build_script()
        
        # ECS task definition
        files['infrastructure/ecs-task-definition.json'] = self._generate_ecs_task_definition(
            requirements, architecture
        )
        
        return files
    
    async def _generate_strands_files(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any],
        implementation: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate Strands agent specification files"""
        files = {}
        
        # Strands specification
        strands_spec = {
            'name': requirements.get('use_case', 'custom_agent'),
            'description': requirements.get('description', ''),
            'version': '1.0.0',
            'capabilities': architecture.get('capabilities', []),
            'tools': architecture.get('tools', []),
            'mcps': architecture.get('mcps', []),
            'aws_services': architecture.get('aws_services', [])
        }
        
        files['strands/agent-spec.json'] = json.dumps(strands_spec, indent=2)
        files['strands/README.md'] = self._generate_strands_readme(strands_spec)
        
        return files
    
    async def _generate_documentation(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any],
        implementation: Dict[str, Any]
    ) -> Dict[str, str]:
        """Generate documentation files"""
        files = {}
        
        use_case = requirements.get('use_case', 'custom_agent')
        
        # Main README
        files['README.md'] = self._generate_readme(requirements, architecture, implementation)
        
        # Architecture documentation
        files['docs/ARCHITECTURE.md'] = self._generate_architecture_doc(architecture)
        
        # API documentation
        files['docs/API.md'] = self._generate_api_doc(requirements, architecture)
        
        # Deployment guide
        files['docs/DEPLOYMENT.md'] = self._generate_deployment_doc(requirements, architecture)
        
        # Cost analysis
        files['docs/COST_ANALYSIS.md'] = self._generate_cost_doc(architecture)
        
        # Security guide
        files['docs/SECURITY.md'] = self._generate_security_doc(architecture)
        
        return files
    
    def _generate_main_agent_code(
        self,
        use_case: str,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Generate main agent code"""
        class_name = ''.join(word.capitalize() for word in use_case.split('_'))
        
        return f'''#!/usr/bin/env python3
"""
{class_name} Agent
Generated by Agent Builder Platform

{requirements.get('description', 'Custom agent implementation')}
"""

import logging
import asyncio
from typing import Dict, Any, Optional
from config import Config
from aws_integration import AWSIntegration
from utils import validate_input, format_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class {class_name}Agent:
    """
    {class_name} Agent Implementation
    
    AWS Services: {', '.join(architecture.get('aws_services', []))}
    MCPs: {', '.join(architecture.get('mcps', []))}
    """
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize agent"""
        self.config = config or Config()
        self.aws = AWSIntegration(self.config)
        logger.info(f"{{self.__class__.__name__}} initialized")
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process incoming request
        
        Args:
            request: Request data with 'type' and 'data' fields
            
        Returns:
            Response dictionary with status and result
        """
        try:
            # Validate input
            if not validate_input(request):
                return format_response('error', None, 'Invalid request format')
            
            request_type = request.get('type')
            data = request.get('data', {{}})
            
            logger.info(f"Processing request type: {{request_type}}")
            
            # Route to appropriate handler
            if request_type == 'query':
                result = await self._handle_query(data)
            elif request_type == 'action':
                result = await self._handle_action(data)
            else:
                result = await self._handle_default(data)
            
            return format_response('success', result)
            
        except Exception as e:
            logger.error(f"Error processing request: {{e}}")
            return format_response('error', None, str(e))
    
    async def _handle_query(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle query requests"""
        # Implement query logic here
        return {{'message': 'Query processed', 'data': data}}
    
    async def _handle_action(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle action requests"""
        # Implement action logic here
        return {{'message': 'Action executed', 'data': data}}
    
    async def _handle_default(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle default requests"""
        return {{'message': 'Request processed', 'data': data}}


async def main():
    """Main entry point"""
    agent = {class_name}Agent()
    
    # Example request
    request = {{
        'type': 'query',
        'data': {{'message': 'Hello, agent!'}}
    }}
    
    result = await agent.process_request(request)
    print(f"Result: {{result}}")


if __name__ == "__main__":
    asyncio.run(main())
'''
    
    def _generate_config_code(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Generate configuration code"""
        return '''#!/usr/bin/env python3
"""
Configuration Management
"""

import os
from typing import Dict, Any
from dataclasses import dataclass


@dataclass
class Config:
    """Application configuration"""
    
    # Environment
    environment: str = os.getenv('ENVIRONMENT', 'development')
    log_level: str = os.getenv('LOG_LEVEL', 'INFO')
    
    # AWS Configuration
    aws_region: str = os.getenv('AWS_REGION', 'us-east-1')
    aws_account_id: str = os.getenv('AWS_ACCOUNT_ID', '')
    
    # Application Settings
    timeout_seconds: int = int(os.getenv('TIMEOUT_SECONDS', '300'))
    max_retries: int = int(os.getenv('MAX_RETRIES', '3'))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'environment': self.environment,
            'log_level': self.log_level,
            'aws_region': self.aws_region,
            'timeout_seconds': self.timeout_seconds,
            'max_retries': self.max_retries
        }
'''
    
    def _generate_aws_integration_code(self, aws_services: List[str]) -> str:
        """Generate AWS integration code"""
        return f'''#!/usr/bin/env python3
"""
AWS Service Integration
Services: {', '.join(aws_services)}
"""

import logging
import boto3
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class AWSIntegration:
    """AWS service integration handler"""
    
    def __init__(self, config):
        """Initialize AWS clients"""
        self.config = config
        self.clients = {{}}
        self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize AWS service clients"""
        services = {aws_services}
        
        for service in services:
            try:
                self.clients[service] = boto3.client(
                    service,
                    region_name=self.config.aws_region
                )
                logger.info(f"Initialized AWS client: {{service}}")
            except Exception as e:
                logger.error(f"Failed to initialize {{service}}: {{e}}")
    
    async def invoke_service(
        self,
        service: str,
        operation: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Invoke AWS service operation
        
        Args:
            service: AWS service name
            operation: Operation to perform
            params: Operation parameters
            
        Returns:
            Operation result
        """
        try:
            if service not in self.clients:
                raise ValueError(f"Service not initialized: {{service}}")
            
            client = self.clients[service]
            method = getattr(client, operation)
            result = method(**params)
            
            return {{'status': 'success', 'result': result}}
            
        except ClientError as e:
            logger.error(f"AWS service error: {{e}}")
            return {{'status': 'error', 'error': str(e)}}
        except Exception as e:
            logger.error(f"Unexpected error: {{e}}")
            return {{'status': 'error', 'error': str(e)}}
'''
    
    def _generate_mcp_integration_code(self, mcps: List[str]) -> str:
        """Generate MCP integration code"""
        return f'''#!/usr/bin/env python3
"""
MCP Integration
MCPs: {', '.join(mcps)}
"""

import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


class MCPIntegration:
    """MCP integration handler"""
    
    def __init__(self):
        """Initialize MCP connections"""
        self.mcps = {mcps}
        logger.info(f"MCP integration initialized with: {{self.mcps}}")
    
    async def query_mcp(
        self,
        mcp_name: str,
        query: str,
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Query MCP server
        
        Args:
            mcp_name: MCP server name
            query: Query string
            context: Optional context
            
        Returns:
            Query result
        """
        try:
            if mcp_name not in self.mcps:
                raise ValueError(f"MCP not configured: {{mcp_name}}")
            
            # Implement MCP query logic here
            logger.info(f"Querying MCP: {{mcp_name}}")
            
            return {{
                'status': 'success',
                'mcp': mcp_name,
                'result': 'Query result placeholder'
            }}
            
        except Exception as e:
            logger.error(f"MCP query failed: {{e}}")
            return {{'status': 'error', 'error': str(e)}}
'''
    
    def _generate_utils_code(self) -> str:
        """Generate utility functions"""
        return '''#!/usr/bin/env python3
"""
Utility Functions
"""

from typing import Dict, Any, Optional


def validate_input(request: Dict[str, Any]) -> bool:
    """
    Validate request input
    
    Args:
        request: Request dictionary
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = ['type', 'data']
    return all(field in request for field in required_fields)


def format_response(
    status: str,
    data: Any,
    error: Optional[str] = None
) -> Dict[str, Any]:
    """
    Format standard response
    
    Args:
        status: Response status
        data: Response data
        error: Optional error message
        
    Returns:
        Formatted response dictionary
    """
    response = {
        'status': status,
        'data': data
    }
    
    if error:
        response['error'] = error
    
    return response


def sanitize_input(text: str) -> str:
    """
    Sanitize user input
    
    Args:
        text: Input text
        
    Returns:
        Sanitized text
    """
    # Implement sanitization logic
    return text.strip()
'''
    
    def _generate_requirements_txt(self, aws_services: List[str], mcps: List[str]) -> str:
        """Generate requirements.txt"""
        requirements = [
            '# Python Dependencies',
            'boto3>=1.28.0',
            'botocore>=1.31.0',
            'asyncio>=3.4.3',
            'python-dotenv>=1.0.0',
            ''
        ]
        
        if any('bedrock' in s.lower() for s in aws_services):
            requirements.append('anthropic>=0.3.0')
        
        if mcps:
            requirements.append('# MCP Integration')
            requirements.append('mcp>=0.1.0')
        
        requirements.extend([
            '',
            '# Testing',
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.0',
            'pytest-cov>=4.1.0'
        ])
        
        return '\n'.join(requirements)
    
    def _generate_env_template(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Generate .env template"""
        return f'''# Environment Configuration Template

# Environment
ENVIRONMENT=development
LOG_LEVEL=INFO

# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=your-account-id

# Application Settings
TIMEOUT_SECONDS=300
MAX_RETRIES=3

# Agent Configuration
AGENT_NAME={requirements.get('use_case', 'custom_agent')}
AGENT_VERSION=1.0.0

# Add your custom environment variables below
'''
    
    def _generate_test_code(self, use_case: str) -> str:
        """Generate test code"""
        class_name = ''.join(word.capitalize() for word in use_case.split('_'))
        
        return f'''#!/usr/bin/env python3
"""
Unit Tests for {class_name} Agent
"""

import pytest
import asyncio
from agent import {class_name}Agent


@pytest.fixture
def agent():
    """Create agent instance for testing"""
    return {class_name}Agent()


def test_agent_initialization(agent):
    """Test agent initialization"""
    assert agent is not None
    assert agent.config is not None
    assert agent.aws is not None


@pytest.mark.asyncio
async def test_process_request_query(agent):
    """Test query request processing"""
    request = {{
        'type': 'query',
        'data': {{'message': 'test query'}}
    }}
    
    result = await agent.process_request(request)
    assert result['status'] == 'success'
    assert 'data' in result


@pytest.mark.asyncio
async def test_process_request_invalid(agent):
    """Test invalid request handling"""
    request = {{'invalid': 'request'}}
    
    result = await agent.process_request(request)
    assert result['status'] == 'error'


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
'''
    
    def _generate_integration_test_code(self, use_case: str, aws_services: List[str]) -> str:
        """Generate integration test code"""
        return f'''#!/usr/bin/env python3
"""
Integration Tests
Tests AWS service integration
"""

import pytest
import asyncio
from agent import {(''.join(word.capitalize() for word in use_case.split('_')))}Agent


@pytest.fixture
def agent():
    """Create agent for integration testing"""
    return {(''.join(word.capitalize() for word in use_case.split('_')))}Agent()


@pytest.mark.asyncio
@pytest.mark.integration
async def test_aws_integration(agent):
    """Test AWS service integration"""
    # Add AWS integration tests here
    assert agent.aws is not None
    assert len(agent.aws.clients) > 0


@pytest.mark.asyncio
@pytest.mark.integration
async def test_end_to_end_workflow(agent):
    """Test complete workflow"""
    request = {{
        'type': 'query',
        'data': {{'test': 'end-to-end'}}
    }}
    
    result = await agent.process_request(request)
    assert result['status'] == 'success'


if __name__ == "__main__":
    pytest.main([__file__, '-v', '-m', 'integration'])
'''
    
    async def generate_deployment_scripts(
        self,
        agent_id: str,
        workflow_data: Dict[str, Any],
        deployment_target: DeploymentTarget = DeploymentTarget.AWS_LAMBDA
    ) -> Dict[str, str]:
        """Generate deployment scripts"""
        scripts = {}
        
        if deployment_target == DeploymentTarget.AWS_LAMBDA:
            scripts['scripts/deploy.sh'] = "#!/bin/bash\necho \"Deploying to Lambda...\""
        elif deployment_target == DeploymentTarget.DOCKER:
            scripts['scripts/deploy.sh'] = "#!/bin/bash\ndocker build -t agent ."
        else:
            scripts['scripts/deploy.sh'] = "#!/bin/bash\necho \"Deploying...\""
        
        return scripts
    
    def _generate_cloudformation_template(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Generate CloudFormation template"""
        use_case = requirements.get('use_case', 'custom-agent')
        aws_services = architecture.get('aws_services', [])
        
        template = f'''AWSTemplateFormatVersion: '2010-09-09'
Description: '{use_case} Agent Infrastructure'

Parameters:
  Environment:
    Type: String
    Default: development
    AllowedValues:
      - development
      - staging
      - production

Resources:
  AgentFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub '${{Environment}}-agent-function'
      Runtime: python3.11
      Handler: agent.handler
      Role: !GetAtt AgentExecutionRole.Arn
      Timeout: 300
      MemorySize: 512

  AgentExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: lambda.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

Outputs:
  AgentFunctionArn:
    Description: Agent Lambda Function ARN
    Value: !GetAtt AgentFunction.Arn
'''
        return template
    
    def _generate_terraform_main(
        self,
        requirements: Dict[str, Any],
        architecture: Dict[str, Any]
    ) -> str:
        """Generate Terraform main configuration"""
        return '''terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_lambda_function" "agent" {
  filename      = "deployment-package.zip"
  function_name = "$${var.environment}-agent-function"
  role          = aws_iam_role.agent_execution.arn
  handler       = "agent.handler"
  runtime       = "python3.11"
}
'''
    
    def _generate_terraform_variables(self) -> str:
        """Generate Terraform variables"""
        return '''variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}
'''
    
    def _generate_terraform_outputs(self) -> str:
        """Generate Terraform outputs"""
        return '''output "function_arn" {
  description = "Lambda function ARN"
  value       = aws_lambda_function.agent.arn
}
'''
    
    def _generate_deploy_script(self) -> str:
        """Generate deployment script"""
        return '''#!/bin/bash
set -e
echo "Deploying infrastructure..."
aws cloudformation deploy --template-file cloudformation-template.yaml --stack-name agent-stack --capabilities CAPABILITY_IAM
echo "Deployment complete!"
'''
    
    def _generate_teardown_script(self) -> str:
        """Generate teardown script"""
        return '''#!/bin/bash
set -e
echo "Tearing down infrastructure..."
aws cloudformation delete-stack --stack-name agent-stack
echo "Teardown complete!"
'''
    
    async def create_export_archive(self, export_package: Dict[str, Any]) -> bytes:
        """Create ZIP archive"""
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file_path, content in export_package['files'].items():
                zip_file.writestr(file_path, str(content))
            
            metadata_json = json.dumps(export_package['metadata'], indent=2)
            zip_file.writestr('metadata.json', metadata_json)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()


# Singleton instance
_export_service: Optional[ExportService] = None


def get_export_service() -> ExportService:
    """Get export service instance (singleton)"""
    global _export_service
    if _export_service is None:
        _export_service = ExportService()
    return _export_service