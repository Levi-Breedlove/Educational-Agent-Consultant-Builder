# AWS Service Registry for AI Agents

## Purpose
This document provides a definitive reference for AI agents and LLMs to accurately identify, select, and use AWS services in architecture diagrams.

## Service Identification System

### Service Node Structure
```typescript
interface ServiceNode {
  id: string              // Unique identifier within template
  name: string            // Official AWS service name
  icon: ComponentType     // AWS icon component
  type: 'aws' | 'generic' // Service type marker
  description: string     // Service purpose
  x: number              // X coordinate
  y: number              // Y coordinate
}
```

### Type System
- **`type: 'aws'`** - Official AWS service with icon
- **`type: 'generic'`** - Non-AWS component (Client, User, External System)

## Official AWS Service Names

### ✅ CORRECT Names (Use These)
| Service | Official Name | Icon Component |
|---------|--------------|----------------|
| Lambda | **AWS Lambda** | `ArchitectureServiceAWSLambda` |
| S3 | **Amazon S3** | `ArchitectureServiceAmazonSimpleStorageService` |
| DynamoDB | **Amazon DynamoDB** | `ArchitectureServiceAmazonDynamoDB` |
| API Gateway | **Amazon API Gateway** | `ArchitectureServiceAmazonAPIGateway` |
| CloudWatch | **Amazon CloudWatch** | `ArchitectureServiceAmazonCloudWatch` |
| ECS | **Amazon ECS Fargate** | `ArchitectureServiceAmazonElasticContainerService` |
| ALB | **Elastic Load Balancing** | `ArchitectureServiceElasticLoadBalancing` |
| RDS | **Amazon RDS** | `ArchitectureServiceAmazonRDS` |
| EventBridge | **Amazon EventBridge** | `ArchitectureServiceAmazonEventBridge` |
| SQS | **Amazon SQS** | `ArchitectureServiceAmazonSimpleQueueService` |
| SNS | **Amazon SNS** | `ArchitectureServiceAmazonSimpleNotificationService` |
| Bedrock | **Amazon Bedrock** | `ArchitectureServiceAmazonBedrock` |
| OpenSearch | **Amazon OpenSearch** | `ArchitectureServiceAmazonOpenSearchService` |
| Glue | **AWS Glue** | `ArchitectureServiceAWSGlue` |
| Athena | **Amazon Athena** | `ArchitectureServiceAmazonAthena` |
| QuickSight | **Amazon QuickSight** | `ArchitectureServiceAmazonQuickSight` |
| IAM | **AWS IAM** | `ArchitectureServiceAWSIdentityandAccessManagement` |
| VPC | **Amazon VPC** | `ArchitectureGroupVirtualprivatecloudVPC` |
| Cognito | **Amazon Cognito** | `ArchitectureServiceAmazonCognito` |

### ❌ INCORRECT Names (Never Use)
- ~~Lambda~~ → Use **AWS Lambda**
- ~~S3~~ → Use **Amazon S3**
- ~~DynamoDB~~ → Use **Amazon DynamoDB**
- ~~API Gateway~~ → Use **Amazon API Gateway**
- ~~SQS~~ → Use **Amazon SQS**
- ~~SNS~~ → Use **Amazon SNS**
- ~~RDS~~ → Use **Amazon RDS**
- ~~IAM~~ → Use **AWS IAM**
- ~~VPC~~ → Use **Amazon VPC**
- ~~ALB~~ → Use **Elastic Load Balancing**
- ~~ECS~~ → Use **Amazon ECS Fargate**

## Service Categories

### Compute
- **AWS Lambda** - Serverless compute
- **Amazon ECS Fargate** - Container orchestration

### Storage
- **Amazon S3** - Object storage
- **Amazon DynamoDB** - NoSQL database
- **Amazon RDS** - Relational database

### Networking
- **Amazon API Gateway** - REST/HTTP API management
- **Elastic Load Balancing** - Load distribution
- **Amazon VPC** - Virtual private cloud

### Integration
- **Amazon EventBridge** - Event bus
- **Amazon SQS** - Message queue
- **Amazon SNS** - Pub/sub messaging

### Monitoring
- **Amazon CloudWatch** - Monitoring and logging

### AI/ML
- **Amazon Bedrock** - Foundation models
- **Amazon OpenSearch** - Search and analytics

### Analytics
- **AWS Glue** - ETL service
- **Amazon Athena** - SQL queries
- **Amazon QuickSight** - Business intelligence

### Security
- **AWS IAM** - Identity and access management
- **Amazon Cognito** - User authentication

## Architecture Patterns

### 1. Serverless REST API
**Services**: Amazon API Gateway → AWS Lambda → Amazon DynamoDB
**Use Case**: Scalable REST APIs without server management

### 2. Container Application
**Services**: Elastic Load Balancing → Amazon ECS Fargate → Amazon RDS
**Use Case**: Containerized applications with managed infrastructure

### 3. Event-Driven Processing
**Services**: Amazon EventBridge → AWS Lambda → Amazon SQS → Amazon DynamoDB
**Use Case**: Asynchronous event processing

### 4. AI Agent Platform
**Services**: Amazon API Gateway → AWS Lambda → Amazon Bedrock → Amazon OpenSearch
**Use Case**: Intelligent applications with LLMs

### 5. Data Analytics Pipeline
**Services**: Amazon S3 → AWS Glue → Amazon Athena → Amazon QuickSight
**Use Case**: Data transformation and visualization

### 6. Microservices Architecture
**Services**: Amazon API Gateway → Multiple AWS Lambda → Amazon DynamoDB + Amazon SQS
**Use Case**: Distributed service architecture

## AI Agent Guidelines

### Service Selection Rules

1. **Always use official AWS names**
   - Include "Amazon", "AWS", or "Elastic" prefix
   - Never use abbreviations alone

2. **Set correct type marker**
   ```typescript
   type: 'aws'  // For AWS services
   type: 'generic'  // For external components
   ```

3. **Provide clear descriptions**
   - Explain the service's role in the architecture
   - Be specific about functionality

4. **Use appropriate icons**
   - Match icon component to service name
   - Import from `aws-react-icons/icons/`

5. **Follow naming conventions**
   - Service IDs: lowercase with hyphens (`api-gateway`, `lambda-processor`)
   - Service names: Official AWS names
   - Descriptions: Clear, concise purpose

### Validation Checklist

Before generating an architecture:
- [ ] All AWS services use official names
- [ ] All services have `type: 'aws'` or `type: 'generic'`
- [ ] All services have descriptions
- [ ] All services have valid icon components
- [ ] All connections reference existing service IDs
- [ ] No duplicate service IDs within template
- [ ] Service positions are non-negative
- [ ] Connection labels are descriptive

### Confidence Scoring

**95-100% Confidence**: 
- Official AWS service names used
- Correct icon components
- Valid architecture pattern
- All services properly typed

**90-94% Confidence**:
- Minor naming inconsistencies
- Missing descriptions
- Suboptimal positioning

**Below 90%**:
- Incorrect service names
- Missing type markers
- Invalid connections
- Wrong icon components

## Testing

Run validation tests:
```bash
npm test AWSServiceValidation.test.tsx
```

Tests verify:
- ✅ Official AWS service names
- ✅ Correct type markers
- ✅ Valid icon components
- ✅ Unique service IDs
- ✅ Valid connections
- ✅ Descriptive labels
- ✅ Proper categorization

## Integration with Agent Core

### For AWS Solutions Architect Agent

```python
# When generating architecture diagrams
def generate_architecture(requirements):
    services = []
    
    # Use official names
    if needs_compute:
        services.append({
            "id": "lambda-function",
            "name": "AWS Lambda",  # ✅ Official name
            "type": "aws",
            "icon": "ArchitectureServiceAWSLambda",
            "description": "Serverless compute for business logic"
        })
    
    if needs_storage:
        services.append({
            "id": "dynamodb-table",
            "name": "Amazon DynamoDB",  # ✅ Official name
            "type": "aws",
            "icon": "ArchitectureServiceAmazonDynamoDB",
            "description": "NoSQL database for application data"
        })
    
    return {
        "services": services,
        "confidence": calculate_confidence(services)
    }
```

### Confidence Calculation

```python
def calculate_confidence(services):
    score = 100
    
    for service in services:
        # Check official naming
        if not service["name"].startswith(("Amazon", "AWS", "Elastic")):
            score -= 10
        
        # Check type marker
        if "type" not in service:
            score -= 5
        
        # Check description
        if not service.get("description"):
            score -= 3
        
        # Check icon
        if not service.get("icon"):
            score -= 5
    
    return max(score, 0)
```

## Summary

This registry ensures:
- ✅ 100% accurate service identification
- ✅ Consistent naming across all templates
- ✅ Machine-readable service metadata
- ✅ Validation through automated tests
- ✅ Clear guidelines for AI agents
- ✅ Confidence scoring for architecture quality

**Result**: AI agents can confidently generate accurate AWS architectures with proper service identification and official naming conventions.
