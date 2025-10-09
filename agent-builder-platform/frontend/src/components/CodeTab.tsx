import { Box, Typography, Alert, AlertTitle, CircularProgress } from '@mui/material'
import { Code as CodeIcon } from '@mui/icons-material'
import CodeWorkspace from './CodeWorkspace'
import { useSelector } from 'react-redux'
import type { RootState } from '../store'

// TEMPORARY: Mock generated code data for visual testing
// This will be replaced with real API data from export service
const MOCK_GENERATED_FILES = [
  {
    path: '/agent-core/main.py',
    content: `"""
Main agent orchestrator for the custom agent.
This file coordinates the agent workflow and manages state.
"""
import asyncio
from typing import Dict, Any, List
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Configuration for the agent."""
    name: str
    description: str
    capabilities: List[str]
    aws_region: str = 'us-east-1'


class AgentOrchestrator:
    """Main orchestrator for agent operations."""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.state: Dict[str, Any] = {}
        logger.info(f"Initialized agent: {config.name}")
    
    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """
        Process a user request through the agent workflow.
        
        Args:
            user_input: The user's input text
            
        Returns:
            Dict containing the agent's response
        """
        try:
            # Validate input
            if not user_input or not user_input.strip():
                raise ValueError("Input cannot be empty")
            
            # Process through workflow
            result = await self._execute_workflow(user_input)
            
            return {
                'success': True,
                'response': result,
                'metadata': {
                    'agent': self.config.name,
                    'timestamp': asyncio.get_event_loop().time()
                }
            }
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    async def _execute_workflow(self, input_text: str) -> str:
        """Execute the main agent workflow."""
        # Placeholder for actual workflow logic
        return f"Processed: {input_text}"


if __name__ == '__main__':
    # Example usage
    config = AgentConfig(
        name='CustomAgent',
        description='A custom agent built with Agent Builder Platform',
        capabilities=['text_processing', 'data_analysis']
    )
    
    orchestrator = AgentOrchestrator(config)
    asyncio.run(orchestrator.process_request("Hello, agent!"))
`,
    language: 'python',
  },
  {
    path: '/infrastructure/cloudformation.yaml',
    content: `AWSTemplateFormatVersion: '2010-09-09'
Description: 'Infrastructure for Custom Agent - ECS Fargate, DynamoDB, S3'

Parameters:
  ProjectName:
    Type: String
    Default: custom-agent
    Description: Name of the project
  
  Environment:
    Type: String
    Default: dev
    AllowedValues:
      - dev
      - staging
      - prod
    Description: Environment name

Resources:
  # VPC Configuration
  VPC:
    Type: AWS::EC2::VPC
    Properties:
      CidrBlock: 10.0.0.0/16
      EnableDnsHostnames: true
      EnableDnsSupport: true
      Tags:
        - Key: Name
          Value: !Sub '\${ProjectName}-vpc-\${Environment}'

  # Public Subnets
  PublicSubnet1:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.1.0/24
      AvailabilityZone: !Select [0, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '\${ProjectName}-public-subnet-1-\${Environment}'

  PublicSubnet2:
    Type: AWS::EC2::Subnet
    Properties:
      VpcId: !Ref VPC
      CidrBlock: 10.0.2.0/24
      AvailabilityZone: !Select [1, !GetAZs '']
      MapPublicIpOnLaunch: true
      Tags:
        - Key: Name
          Value: !Sub '\${ProjectName}-public-subnet-2-\${Environment}'

  # Internet Gateway
  InternetGateway:
    Type: AWS::EC2::InternetGateway
    Properties:
      Tags:
        - Key: Name
          Value: !Sub '\${ProjectName}-igw-\${Environment}'

  AttachGateway:
    Type: AWS::EC2::VPCGatewayAttachment
    Properties:
      VpcId: !Ref VPC
      InternetGatewayId: !Ref InternetGateway

  # DynamoDB Table for State Management
  StateTable:
    Type: AWS::DynamoDB::Table
    Properties:
      TableName: !Sub '\${ProjectName}-state-\${Environment}'
      BillingMode: PAY_PER_REQUEST
      AttributeDefinitions:
        - AttributeName: agent_id
          AttributeType: S
        - AttributeName: timestamp
          AttributeType: N
      KeySchema:
        - AttributeName: agent_id
          KeyType: HASH
        - AttributeName: timestamp
          KeyType: RANGE
      StreamSpecification:
        StreamViewType: NEW_AND_OLD_IMAGES
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # S3 Bucket for Artifacts
  ArtifactsBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub '\${ProjectName}-artifacts-\${Environment}-\${AWS::AccountId}'
      BucketEncryption:
        ServerSideEncryptionConfiguration:
          - ServerSideEncryptionByDefault:
              SSEAlgorithm: AES256
      PublicAccessBlockConfiguration:
        BlockPublicAcls: true
        BlockPublicPolicy: true
        IgnorePublicAcls: true
        RestrictPublicBuckets: true
      VersioningConfiguration:
        Status: Enabled
      Tags:
        - Key: Environment
          Value: !Ref Environment

  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub '\${ProjectName}-cluster-\${Environment}'
      CapacityProviders:
        - FARGATE
        - FARGATE_SPOT
      DefaultCapacityProviderStrategy:
        - CapacityProvider: FARGATE
          Weight: 1
        - CapacityProvider: FARGATE_SPOT
          Weight: 4
      Tags:
        - Key: Environment
          Value: !Ref Environment

Outputs:
  VPCId:
    Description: VPC ID
    Value: !Ref VPC
    Export:
      Name: !Sub '\${ProjectName}-vpc-id-\${Environment}'

  StateTableName:
    Description: DynamoDB State Table Name
    Value: !Ref StateTable
    Export:
      Name: !Sub '\${ProjectName}-state-table-\${Environment}'

  ArtifactsBucketName:
    Description: S3 Artifacts Bucket Name
    Value: !Ref ArtifactsBucket
    Export:
      Name: !Sub '\${ProjectName}-artifacts-bucket-\${Environment}'

  ECSClusterName:
    Description: ECS Cluster Name
    Value: !Ref ECSCluster
    Export:
      Name: !Sub '\${ProjectName}-ecs-cluster-\${Environment}'
`,
    language: 'yaml',
  },
  {
    path: '/config/agent-config.json',
    content: `{
  "agent": {
    "name": "CustomAgent",
    "version": "1.0.0",
    "description": "A custom agent built with Agent Builder Platform",
    "capabilities": [
      "text_processing",
      "data_analysis",
      "aws_integration"
    ]
  },
  "aws": {
    "region": "us-east-1",
    "services": {
      "bedrock": {
        "model": "anthropic.claude-3-sonnet-20240229-v1:0",
        "max_tokens": 4096,
        "temperature": 0.7
      },
      "dynamodb": {
        "table_name": "custom-agent-state-dev",
        "read_capacity": 5,
        "write_capacity": 5
      },
      "s3": {
        "bucket_name": "custom-agent-artifacts-dev",
        "encryption": "AES256"
      }
    }
  },
  "monitoring": {
    "cloudwatch": {
      "enabled": true,
      "log_group": "/aws/ecs/custom-agent",
      "metrics_namespace": "CustomAgent"
    },
    "xray": {
      "enabled": true,
      "sampling_rate": 0.1
    }
  },
  "security": {
    "iam_role": "arn:aws:iam::123456789012:role/CustomAgentRole",
    "kms_key": "arn:aws:kms:us-east-1:123456789012:key/12345678-1234-1234-1234-123456789012",
    "vpc_config": {
      "subnet_ids": [
        "subnet-12345678",
        "subnet-87654321"
      ],
      "security_group_ids": [
        "sg-12345678"
      ]
    }
  },
  "performance": {
    "timeout_seconds": 300,
    "memory_mb": 2048,
    "cpu_units": 1024,
    "auto_scaling": {
      "min_tasks": 1,
      "max_tasks": 10,
      "target_cpu_utilization": 70
    }
  }
}
`,
    language: 'json',
  },
  {
    path: '/tests/test_orchestrator.py',
    content: `"""
Unit tests for the agent orchestrator.
"""
import pytest
import asyncio
from agent_core.main import AgentOrchestrator, AgentConfig


@pytest.fixture
def agent_config():
    """Create a test agent configuration."""
    return AgentConfig(
        name='TestAgent',
        description='Test agent for unit testing',
        capabilities=['test_capability'],
        aws_region='us-east-1'
    )


@pytest.fixture
def orchestrator(agent_config):
    """Create an orchestrator instance for testing."""
    return AgentOrchestrator(agent_config)


class TestAgentOrchestrator:
    """Test suite for AgentOrchestrator."""
    
    @pytest.mark.asyncio
    async def test_initialization(self, orchestrator, agent_config):
        """Test that orchestrator initializes correctly."""
        assert orchestrator.config.name == agent_config.name
        assert orchestrator.config.description == agent_config.description
        assert isinstance(orchestrator.state, dict)
    
    @pytest.mark.asyncio
    async def test_process_request_success(self, orchestrator):
        """Test successful request processing."""
        result = await orchestrator.process_request("Test input")
        
        assert result['success'] is True
        assert 'response' in result
        assert 'metadata' in result
        assert result['metadata']['agent'] == 'TestAgent'
    
    @pytest.mark.asyncio
    async def test_process_request_empty_input(self, orchestrator):
        """Test that empty input is handled correctly."""
        result = await orchestrator.process_request("")
        
        assert result['success'] is False
        assert 'error' in result
        assert 'empty' in result['error'].lower()
    
    @pytest.mark.asyncio
    async def test_process_request_whitespace_input(self, orchestrator):
        """Test that whitespace-only input is handled correctly."""
        result = await orchestrator.process_request("   ")
        
        assert result['success'] is False
        assert 'error' in result
    
    @pytest.mark.asyncio
    async def test_workflow_execution(self, orchestrator):
        """Test the internal workflow execution."""
        result = await orchestrator._execute_workflow("Test workflow")
        
        assert isinstance(result, str)
        assert "Test workflow" in result


@pytest.mark.asyncio
async def test_concurrent_requests(orchestrator):
    """Test handling multiple concurrent requests."""
    tasks = [
        orchestrator.process_request(f"Request {i}")
        for i in range(5)
    ]
    
    results = await asyncio.gather(*tasks)
    
    assert len(results) == 5
    assert all(r['success'] for r in results)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
`,
    language: 'python',
  },
  {
    path: '/README.md',
    content: `# Custom Agent

A production-ready agent built with the Agent Builder Platform, leveraging AWS services and best practices.

## Overview

This agent provides text processing and data analysis capabilities, deployed on AWS infrastructure using ECS Fargate, DynamoDB, and S3.

## Features

- **Scalable Architecture**: ECS Fargate with auto-scaling
- **State Management**: DynamoDB for persistent state
- **Artifact Storage**: S3 with encryption and versioning
- **Monitoring**: CloudWatch logs and metrics, X-Ray tracing
- **Security**: IAM roles, KMS encryption, VPC isolation

## Prerequisites

- AWS Account with appropriate permissions
- AWS CLI configured
- Python 3.9+
- Docker (for local testing)

## Quick Start

### 1. Deploy Infrastructure

\`\`\`bash
# Deploy CloudFormation stack
aws cloudformation create-stack \\
  --stack-name custom-agent-dev \\
  --template-body file://infrastructure/cloudformation.yaml \\
  --parameters ParameterKey=Environment,ParameterValue=dev \\
  --capabilities CAPABILITY_IAM

# Wait for stack creation
aws cloudformation wait stack-create-complete \\
  --stack-name custom-agent-dev
\`\`\`

### 2. Install Dependencies

\`\`\`bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
\`\`\`

### 3. Configure Agent

Edit \`config/agent-config.json\` with your AWS resource ARNs and settings.

### 4. Run Locally

\`\`\`bash
# Run the agent
python agent-core/main.py
\`\`\`

### 5. Run Tests

\`\`\`bash
# Run unit tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=agent_core --cov-report=html
\`\`\`

## Architecture

\`\`\`
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       ▼
┌─────────────────────┐
│  Application Load   │
│     Balancer        │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   ECS Fargate       │
│  (Agent Runtime)    │
└──────┬──────────────┘
       │
       ├──────────────┐
       │              │
       ▼              ▼
┌──────────┐   ┌──────────┐
│ DynamoDB │   │    S3    │
│  (State) │   │(Artifacts)│
└──────────┘   └──────────┘
\`\`\`

## Configuration

### Environment Variables

- \`AWS_REGION\`: AWS region (default: us-east-1)
- \`ENVIRONMENT\`: Environment name (dev/staging/prod)
- \`LOG_LEVEL\`: Logging level (default: INFO)

### AWS Resources

- **ECS Cluster**: Runs the agent containers
- **DynamoDB Table**: Stores agent state and session data
- **S3 Bucket**: Stores artifacts and generated outputs
- **CloudWatch**: Logs and metrics
- **IAM Roles**: Least-privilege access control

## Monitoring

### CloudWatch Dashboards

Access metrics at: AWS Console → CloudWatch → Dashboards → custom-agent-dashboard

Key metrics:
- Request count and latency
- Error rates
- CPU and memory utilization
- DynamoDB read/write capacity

### Logs

View logs at: AWS Console → CloudWatch → Log Groups → /aws/ecs/custom-agent

## Security

- All data encrypted at rest (KMS)
- All data encrypted in transit (TLS)
- VPC isolation with security groups
- IAM roles with least-privilege access
- No hardcoded credentials

## Cost Optimization

- Uses AWS Free Tier where possible
- ECS Fargate Spot for cost savings (80% of capacity)
- DynamoDB on-demand pricing
- S3 lifecycle policies for old artifacts
- CloudWatch log retention policies

**Estimated Monthly Cost**: $15-30 (depending on usage)

## Troubleshooting

### Agent not starting

1. Check CloudWatch logs for errors
2. Verify IAM role permissions
3. Ensure VPC and security group configuration

### High latency

1. Check ECS task CPU/memory utilization
2. Review DynamoDB capacity metrics
3. Enable X-Ray tracing for detailed analysis

### Deployment failures

1. Validate CloudFormation template
2. Check AWS service quotas
3. Verify IAM permissions

## Support

For issues or questions:
- Check the [documentation](docs/)
- Review [troubleshooting guide](docs/troubleshooting.md)
- Contact support team

## License

MIT License - See LICENSE file for details
`,
    language: 'markdown',
  },
]

interface CodeTabProps {
  agentId?: string
}

export default function CodeTab({ agentId: _agentId }: CodeTabProps) {
  // TODO: Use _agentId to fetch generated code from export service API when backend is ready
  // For now, using mock data for visual testing
  const workflowPhase = useSelector((state: RootState) => state.workflow.currentPhase)
  const phaseStatus = useSelector((state: RootState) => state.workflow.phases)

  // Check if code generation phase is complete
  const isCodeGenerated = phaseStatus.implementation === 'completed'
  const isLoading = phaseStatus.implementation === 'in_progress'

  // Empty state - no code generated yet
  if (!isCodeGenerated && !isLoading) {
    return (
      <Box
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          p: 4,
          textAlign: 'center',
        }}
      >
        <CodeIcon sx={{ fontSize: 64, color: 'text.secondary', mb: 2 }} />
        <Typography variant="h5" gutterBottom color="text.secondary">
          No Code Generated Yet
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 500 }}>
          Complete the requirements and architecture phases to generate your agent code.
          The code will appear here once the implementation phase begins.
        </Typography>
        <Alert severity="info" sx={{ mt: 3, maxWidth: 600 }}>
          <AlertTitle>Current Phase: {workflowPhase}</AlertTitle>
          Continue chatting with the AI consultants to progress through the workflow.
        </Alert>
      </Box>
    )
  }

  // Loading state - code generation in progress
  if (isLoading) {
    return (
      <Box
        sx={{
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          p: 4,
          textAlign: 'center',
        }}
      >
        <CircularProgress size={64} sx={{ mb: 3 }} />
        <Typography variant="h5" gutterBottom>
          Generating Your Agent Code...
        </Typography>
        <Typography variant="body1" color="text.secondary" sx={{ maxWidth: 500 }}>
          The Implementation Guide is creating production-ready code based on your requirements
          and architecture design. This may take a few moments.
        </Typography>
      </Box>
    )
  }

  // Code generated - show workspace
  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column', p: 2 }}>
      <Alert severity="success" sx={{ mb: 2 }}>
        <AlertTitle>Code Generated Successfully</AlertTitle>
        Your production-ready agent code is ready. Browse the files below to explore the
        implementation, infrastructure, configuration, and tests.
      </Alert>

      <Box sx={{ flex: 1, minHeight: 0 }}>
        <CodeWorkspace
          files={MOCK_GENERATED_FILES}
          title="Generated Agent Code"
          showDiff={false}
        />
      </Box>

      <Alert severity="info" sx={{ mt: 2 }}>
        <AlertTitle>Next Steps</AlertTitle>
        Download the code, review the README for deployment instructions, and run the tests
        to validate your agent before deploying to AWS.
      </Alert>
    </Box>
  )
}
