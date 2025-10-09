#!/usr/bin/env python3
"""
Tests for Export and Deployment Endpoints
"""

import pytest
import asyncio
from datetime import datetime
from export_service import ExportService, ExportFormat, DeploymentTarget


@pytest.fixture
def export_service():
    """Create export service instance"""
    return ExportService()


@pytest.fixture
def sample_workflow_data():
    """Sample workflow data for testing"""
    return {
        'requirements': {
            'use_case': 'customer_support_chatbot',
            'description': 'AI-powered customer support chatbot',
            'user_id': 'test-user',
            'experience_level': 'beginner'
        },
        'architecture': {
            'aws_services': ['lambda', 'dynamodb', 's3', 'bedrock'],
            'mcps': ['aws_documentation', 'strands_patterns'],
            'capabilities': ['natural_language_processing', 'data_storage'],
            'tools': ['aws_lambda', 'aws_bedrock'],
            'cost_estimate': '$15-30/month'
        },
        'implementation': {
            'code_generated': True,
            'tests_included': True
        }
    }


@pytest.mark.asyncio
async def test_export_agent_code_format(export_service, sample_workflow_data):
    """Test exporting agent in code format"""
    result = await export_service.export_agent(
        agent_id='test-agent-123',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.CODE,
        include_tests=True
    )
    
    assert result['agent_id'] == 'test-agent-123'
    assert result['export_format'] == 'code'
    assert 'files' in result
    assert 'metadata' in result
    
    # Check for essential code files
    assert 'src/agent.py' in result['files']
    assert 'src/config.py' in result['files']
    assert 'requirements.txt' in result['files']
    assert 'tests/test_agent.py' in result['files']
    
    # Check metadata
    assert result['metadata']['agent_name'] == 'customer_support_chatbot'
    assert result['metadata']['file_count'] > 0


@pytest.mark.asyncio
async def test_export_agent_iac_format(export_service, sample_workflow_data):
    """Test exporting agent in IaC format"""
    result = await export_service.export_agent(
        agent_id='test-agent-456',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.IAC,
        include_tests=False
    )
    
    assert result['export_format'] == 'iac'
    
    # Check for IaC files
    assert 'infrastructure/cloudformation-template.yaml' in result['files']
    assert 'infrastructure/terraform/main.tf' in result['files']
    assert 'infrastructure/deploy.sh' in result['files']
    assert 'infrastructure/teardown.sh' in result['files']


@pytest.mark.asyncio
async def test_export_agent_container_format(export_service, sample_workflow_data):
    """Test exporting agent in container format"""
    result = await export_service.export_agent(
        agent_id='test-agent-789',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.CONTAINER,
        include_tests=False
    )
    
    assert result['export_format'] == 'container'
    
    # Check for container files
    assert 'Dockerfile' in result['files']
    assert 'docker-compose.yml' in result['files']
    assert 'scripts/build-docker.sh' in result['files']
    assert 'infrastructure/ecs-task-definition.json' in result['files']


@pytest.mark.asyncio
async def test_export_agent_strands_format(export_service, sample_workflow_data):
    """Test exporting agent in Strands format"""
    result = await export_service.export_agent(
        agent_id='test-agent-strands',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.STRANDS,
        include_tests=False
    )
    
    assert result['export_format'] == 'strands'
    
    # Check for Strands files
    assert 'strands/agent-spec.json' in result['files']
    assert 'strands/README.md' in result['files']


@pytest.mark.asyncio
async def test_export_agent_complete_format(export_service, sample_workflow_data):
    """Test exporting agent in complete format"""
    result = await export_service.export_agent(
        agent_id='test-agent-complete',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.COMPLETE,
        include_tests=True
    )
    
    assert result['export_format'] == 'complete'
    
    # Check for all file types
    assert 'src/agent.py' in result['files']  # Code
    assert 'infrastructure/cloudformation-template.yaml' in result['files']  # IaC
    assert 'Dockerfile' in result['files']  # Container
    assert 'strands/agent-spec.json' in result['files']  # Strands
    assert 'README.md' in result['files']  # Documentation
    
    # Check documentation files
    assert 'docs/ARCHITECTURE.md' in result['files']
    assert 'docs/API.md' in result['files']
    assert 'docs/DEPLOYMENT.md' in result['files']
    assert 'docs/COST_ANALYSIS.md' in result['files']
    assert 'docs/SECURITY.md' in result['files']


@pytest.mark.asyncio
async def test_export_without_tests(export_service, sample_workflow_data):
    """Test exporting agent without tests"""
    result = await export_service.export_agent(
        agent_id='test-agent-no-tests',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.CODE,
        include_tests=False
    )
    
    # Tests should not be included
    assert 'tests/test_agent.py' not in result['files']
    assert result['metadata']['includes_tests'] is False


@pytest.mark.asyncio
async def test_generate_deployment_scripts_lambda(export_service, sample_workflow_data):
    """Test generating Lambda deployment scripts"""
    scripts = await export_service.generate_deployment_scripts(
        agent_id='test-agent-lambda',
        workflow_data=sample_workflow_data,
        deployment_target=DeploymentTarget.AWS_LAMBDA
    )
    
    assert 'deploy-lambda.sh' in scripts
    assert 'package-lambda.sh' in scripts
    
    # Check script content
    assert 'aws lambda' in scripts['deploy-lambda.sh']
    assert 'zip' in scripts['package-lambda.sh']


@pytest.mark.asyncio
async def test_generate_deployment_scripts_ecs(export_service, sample_workflow_data):
    """Test generating ECS deployment scripts"""
    scripts = await export_service.generate_deployment_scripts(
        agent_id='test-agent-ecs',
        workflow_data=sample_workflow_data,
        deployment_target=DeploymentTarget.AWS_ECS
    )
    
    assert 'deploy-ecs.sh' in scripts
    assert 'update-ecs.sh' in scripts
    
    # Check script content
    assert 'aws ecs' in scripts['deploy-ecs.sh']


@pytest.mark.asyncio
async def test_generate_deployment_scripts_docker(export_service, sample_workflow_data):
    """Test generating Docker deployment scripts"""
    scripts = await export_service.generate_deployment_scripts(
        agent_id='test-agent-docker',
        workflow_data=sample_workflow_data,
        deployment_target=DeploymentTarget.DOCKER
    )
    
    assert 'build-docker.sh' in scripts
    assert 'run-docker.sh' in scripts
    
    # Check script content
    assert 'docker build' in scripts['build-docker.sh']
    assert 'docker run' in scripts['run-docker.sh']


@pytest.mark.asyncio
async def test_generate_deployment_scripts_local(export_service, sample_workflow_data):
    """Test generating local deployment scripts"""
    scripts = await export_service.generate_deployment_scripts(
        agent_id='test-agent-local',
        workflow_data=sample_workflow_data,
        deployment_target=DeploymentTarget.LOCAL
    )
    
    assert 'run-local.sh' in scripts
    
    # Check script content
    assert 'python' in scripts['run-local.sh']
    assert 'venv' in scripts['run-local.sh']


@pytest.mark.asyncio
async def test_create_export_archive(export_service, sample_workflow_data):
    """Test creating export archive"""
    # First export the agent
    export_package = await export_service.export_agent(
        agent_id='test-agent-archive',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.COMPLETE,
        include_tests=True
    )
    
    # Create archive
    zip_bytes = await export_service.create_export_archive(export_package)
    
    assert isinstance(zip_bytes, bytes)
    assert len(zip_bytes) > 0
    
    # Verify it's a valid ZIP file
    import zipfile
    import io
    
    zip_buffer = io.BytesIO(zip_bytes)
    with zipfile.ZipFile(zip_buffer, 'r') as zip_file:
        file_list = zip_file.namelist()
        assert len(file_list) > 0
        assert 'metadata.json' in file_list


@pytest.mark.asyncio
async def test_export_with_aws_services(export_service):
    """Test export with various AWS services"""
    workflow_data = {
        'requirements': {
            'use_case': 'data_processor',
            'description': 'Data processing agent'
        },
        'architecture': {
            'aws_services': ['lambda', 'dynamodb', 's3', 'sqs', 'sns'],
            'mcps': ['aws_documentation'],
            'cost_estimate': '$20-40/month'
        },
        'implementation': {}
    }
    
    result = await export_service.export_agent(
        agent_id='test-agent-services',
        workflow_data=workflow_data,
        export_format=ExportFormat.COMPLETE,
        include_tests=True
    )
    
    # Check AWS integration code
    assert 'src/aws_integration.py' in result['files']
    
    # Verify services are mentioned in the code
    aws_code = result['files']['src/aws_integration.py']
    assert 'lambda' in aws_code
    assert 'dynamodb' in aws_code


@pytest.mark.asyncio
async def test_export_with_mcps(export_service):
    """Test export with MCP integration"""
    workflow_data = {
        'requirements': {
            'use_case': 'research_agent',
            'description': 'Research and analysis agent'
        },
        'architecture': {
            'aws_services': ['lambda'],
            'mcps': ['aws_documentation', 'perplexity', 'github_analysis'],
            'cost_estimate': '$10-20/month'
        },
        'implementation': {}
    }
    
    result = await export_service.export_agent(
        agent_id='test-agent-mcps',
        workflow_data=workflow_data,
        export_format=ExportFormat.CODE,
        include_tests=False
    )
    
    # Check MCP integration code
    assert 'src/mcp_integration.py' in result['files']
    
    # Verify MCPs are mentioned
    mcp_code = result['files']['src/mcp_integration.py']
    assert 'aws_documentation' in mcp_code
    assert 'perplexity' in mcp_code


@pytest.mark.asyncio
async def test_deployment_instructions_generation(export_service, sample_workflow_data):
    """Test deployment instructions generation"""
    result = await export_service.export_agent(
        agent_id='test-agent-instructions',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.COMPLETE,
        include_tests=True
    )
    
    assert 'deployment_instructions' in result
    assert isinstance(result['deployment_instructions'], list)
    assert len(result['deployment_instructions']) > 0
    
    # Check for key instruction steps
    instructions_text = ' '.join(result['deployment_instructions'])
    assert 'README' in instructions_text
    assert 'dependencies' in instructions_text
    assert 'tests' in instructions_text


@pytest.mark.asyncio
async def test_export_metadata_completeness(export_service, sample_workflow_data):
    """Test export metadata completeness"""
    result = await export_service.export_agent(
        agent_id='test-agent-metadata',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.COMPLETE,
        include_tests=True
    )
    
    metadata = result['metadata']
    
    # Check all required metadata fields
    assert 'agent_name' in metadata
    assert 'description' in metadata
    assert 'file_count' in metadata
    assert 'export_size_bytes' in metadata
    assert 'aws_services' in metadata
    assert 'mcps' in metadata
    assert 'estimated_cost' in metadata
    assert 'includes_tests' in metadata
    
    # Verify values
    assert metadata['agent_name'] == 'customer_support_chatbot'
    assert metadata['file_count'] > 0
    assert metadata['export_size_bytes'] > 0
    assert metadata['includes_tests'] is True


@pytest.mark.asyncio
async def test_cloudformation_template_generation(export_service, sample_workflow_data):
    """Test CloudFormation template generation"""
    result = await export_service.export_agent(
        agent_id='test-agent-cfn',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.IAC,
        include_tests=False
    )
    
    cfn_template = result['files']['infrastructure/cloudformation-template.yaml']
    
    # Check template structure
    assert 'AWSTemplateFormatVersion' in cfn_template
    assert 'Resources' in cfn_template
    assert 'Outputs' in cfn_template
    
    # Check for AWS resources based on services
    assert 'AgentFunction' in cfn_template  # Lambda
    assert 'AgentTable' in cfn_template  # DynamoDB
    assert 'AgentBucket' in cfn_template  # S3


@pytest.mark.asyncio
async def test_terraform_configuration_generation(export_service, sample_workflow_data):
    """Test Terraform configuration generation"""
    result = await export_service.export_agent(
        agent_id='test-agent-tf',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.IAC,
        include_tests=False
    )
    
    tf_main = result['files']['infrastructure/terraform/main.tf']
    tf_vars = result['files']['infrastructure/terraform/variables.tf']
    tf_outputs = result['files']['infrastructure/terraform/outputs.tf']
    
    # Check Terraform files
    assert 'terraform' in tf_main
    assert 'resource' in tf_main
    assert 'variable' in tf_vars
    assert 'output' in tf_outputs


@pytest.mark.asyncio
async def test_dockerfile_generation(export_service, sample_workflow_data):
    """Test Dockerfile generation"""
    result = await export_service.export_agent(
        agent_id='test-agent-dockerfile',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.CONTAINER,
        include_tests=False
    )
    
    dockerfile = result['files']['Dockerfile']
    
    # Check Dockerfile content
    assert 'FROM python:3.11-slim' in dockerfile
    assert 'WORKDIR' in dockerfile
    assert 'COPY' in dockerfile
    assert 'RUN pip install' in dockerfile
    assert 'CMD' in dockerfile


@pytest.mark.asyncio
async def test_documentation_generation(export_service, sample_workflow_data):
    """Test documentation generation"""
    result = await export_service.export_agent(
        agent_id='test-agent-docs',
        workflow_data=sample_workflow_data,
        export_format=ExportFormat.COMPLETE,
        include_tests=True
    )
    
    # Check README
    readme = result['files']['README.md']
    assert 'customer_support_chatbot' in readme.lower()
    assert 'Overview' in readme
    assert 'Quick Start' in readme
    assert 'Deployment' in readme
    
    # Check architecture doc
    arch_doc = result['files']['docs/ARCHITECTURE.md']
    assert 'Architecture' in arch_doc
    assert 'Components' in arch_doc
    
    # Check cost doc
    cost_doc = result['files']['docs/COST_ANALYSIS.md']
    assert 'Cost' in cost_doc
    assert '$15-30/month' in cost_doc


def test_export_service_singleton():
    """Test export service singleton pattern"""
    from export_service import get_export_service
    
    service1 = get_export_service()
    service2 = get_export_service()
    
    assert service1 is service2


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
