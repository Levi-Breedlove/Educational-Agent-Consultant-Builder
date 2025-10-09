# AWS Service Icon Registry - Complete Reference

## Overview

This document provides a comprehensive reference for all 100+ AWS service icons available in the codebase, organized by category with official naming conventions, descriptions, and use cases.

## Registry Location

**File**: `src/components/AWSServiceIconRegistry.tsx`

**Icon Library**: `aws-react-icons` v3.2.0

## Total Services: 100+

### Service Categories (14)
1. Compute (8 services)
2. Storage (6 services)
3. Database (9 services)
4. Networking (10 services)
5. Security (12 services)
6. AI/ML (12 services)
7. Analytics (10 services)
8. Application Integration (7 services)
9. Management & Governance (10 services)
10. Developer Tools (7 services)
11. Migration & Transfer (5 services)
12. Front-End Web & Mobile (3 services)
13. Media Services (5 services)
14. IoT (4 services)

---

## Complete Service Listing

### 1. COMPUTE SERVICES (8)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `lambda` | **AWS Lambda** | `ArchitectureServiceAWSLambda` | Event-driven processing, API backends, Data transformation |
| `ec2` | **Amazon EC2** | `ArchitectureServiceAmazonEC2` | Web applications, Batch processing, Gaming servers |
| `ecs` | **Amazon ECS** | `ArchitectureServiceAmazonElasticContainerService` | Microservices, Batch jobs, ML model serving |
| `eks` | **Amazon EKS** | `ArchitectureServiceAmazonElasticKubernetesService` | Kubernetes workloads, Cloud-native apps, Hybrid deployments |
| `fargate` | **AWS Fargate** | `ArchitectureServiceAWSFargate` | Serverless containers, Microservices, Batch processing |
| `batch` | **AWS Batch** | `ArchitectureServiceAWSBatch` | Data processing, Scientific computing, Financial modeling |
| `lightsail` | **Amazon Lightsail** | `ArchitectureServiceAmazonLightsail` | Simple web apps, Development environments, Small databases |
| `elastic-beanstalk` | **AWS Elastic Beanstalk** | `ArchitectureServiceAWSElasticBeanstalk` | Web applications, API services, Worker processes |

### 2. STORAGE SERVICES (6)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `s3` | **Amazon S3** | `ArchitectureServiceAmazonSimpleStorageService` | Data lakes, Backup, Static websites, Media storage |
| `ebs` | **Amazon EBS** | `ArchitectureServiceAmazonElasticBlockStore` | Database storage, File systems, Boot volumes |
| `efs` | **Amazon EFS** | `ArchitectureServiceAmazonElasticFileSystem` | Shared file systems, Content management, Web serving |
| `fsx` | **Amazon FSx** | `ArchitectureServiceAmazonFSx` | Windows file shares, Lustre for HPC, NetApp ONTAP |
| `storage-gateway` | **AWS Storage Gateway** | `ArchitectureServiceAWSStorageGateway` | Backup to cloud, Disaster recovery, Cloud migration |
| `backup` | **AWS Backup** | `ArchitectureServiceAWSBackup` | Automated backups, Compliance, Disaster recovery |

### 3. DATABASE SERVICES (9)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `dynamodb` | **Amazon DynamoDB** | `ArchitectureServiceAmazonDynamoDB` | Web applications, Gaming, IoT, Mobile backends |
| `rds` | **Amazon RDS** | `ArchitectureServiceAmazonRDS` | Web applications, E-commerce, Enterprise apps |
| `aurora` | **Amazon Aurora** | `ArchitectureServiceAmazonAurora` | High-performance apps, SaaS applications, Gaming |
| `elasticache` | **Amazon ElastiCache** | `ArchitectureServiceAmazonElastiCache` | Session storage, Caching, Real-time analytics |
| `memorydb` | **Amazon MemoryDB** | `ArchitectureServiceAmazonMemoryDB` | Real-time applications, Leaderboards, Session stores |
| `documentdb` | **Amazon DocumentDB** | `ArchitectureServiceAmazonDocumentDB` | Content management, Catalogs, User profiles |
| `neptune` | **Amazon Neptune** | `ArchitectureServiceAmazonNeptune` | Social networks, Fraud detection, Knowledge graphs |
| `keyspaces` | **Amazon Keyspaces** | `ArchitectureServiceAmazonKeyspaces` | IoT applications, Time-series data, High-throughput apps |
| `timestream` | **Amazon Timestream** | `ArchitectureServiceAmazonTimestream` | IoT analytics, DevOps monitoring, Application metrics |

### 4. NETWORKING & CONTENT DELIVERY (10)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `vpc` | **Amazon VPC** | `ArchitectureServiceAmazonVPC` | Network isolation, Multi-tier applications, Hybrid cloud |
| `cloudfront` | **Amazon CloudFront** | `ArchitectureServiceAmazonCloudFront` | Website acceleration, Video streaming, API acceleration |
| `route53` | **Amazon Route 53** | `ArchitectureServiceAmazonRoute53` | Domain management, Traffic routing, Health checks |
| `api-gateway` | **Amazon API Gateway** | `ArchitectureServiceAmazonAPIGateway` | REST APIs, WebSocket APIs, HTTP APIs |
| `elb` | **Elastic Load Balancing** | `ArchitectureServiceElasticLoadBalancing` | High availability, Auto scaling, Fault tolerance |
| `direct-connect` | **AWS Direct Connect** | `ArchitectureServiceAWSDirectConnect` | Hybrid cloud, Large data transfers, Low latency |
| `app-mesh` | **AWS App Mesh** | `ArchitectureServiceAWSAppMesh` | Microservices, Service mesh, Traffic management |
| `cloud-map` | **AWS Cloud Map** | `ArchitectureServiceAWSCloudMap` | Service discovery, Microservices, Dynamic resources |
| `global-accelerator` | **AWS Global Accelerator** | `ArchitectureServiceAWSGlobalAccelerator` | Global applications, Gaming, VoIP |
| `transit-gateway` | **AWS Transit Gateway** | `ArchitectureServiceAWSTransitGateway` | Network hub, Multi-VPC, Hybrid connectivity |

### 5. SECURITY, IDENTITY & COMPLIANCE (12)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `iam` | **AWS IAM** | `ArchitectureServiceAWSIdentityandAccessManagement` | User management, Access control, Federation |
| `cognito` | **Amazon Cognito** | `ArchitectureServiceAmazonCognito` | User sign-up/sign-in, Social identity, MFA |
| `secrets-manager` | **AWS Secrets Manager** | `ArchitectureServiceAWSSecretsManager` | Database credentials, API keys, Secret rotation |
| `certificate-manager` | **AWS Certificate Manager** | `ArchitectureServiceAWSCertificateManager` | HTTPS websites, SSL certificates, Certificate renewal |
| `kms` | **AWS KMS** | `ArchitectureServiceAWSKeyManagementService` | Data encryption, Key management, Compliance |
| `waf` | **AWS WAF** | `ArchitectureServiceAWSWAF` | DDoS protection, SQL injection prevention, XSS protection |
| `shield` | **AWS Shield** | `ArchitectureServiceAWSShield` | DDoS mitigation, Application protection, Network protection |
| `guardduty` | **Amazon GuardDuty** | `ArchitectureServiceAmazonGuardDuty` | Threat detection, Security monitoring, Anomaly detection |
| `inspector` | **Amazon Inspector** | `ArchitectureServiceAmazonInspector` | Vulnerability scanning, Compliance checking, Security assessment |
| `macie` | **Amazon Macie** | `ArchitectureServiceAmazonMacie` | Data discovery, PII detection, Data classification |
| `security-hub` | **AWS Security Hub** | `ArchitectureServiceAWSSecurityHub` | Security posture, Compliance monitoring, Finding aggregation |
| `cloudhsm` | **AWS CloudHSM** | `ArchitectureServiceAWSCloudHSM` | Key storage, Cryptographic operations, Compliance |

### 6. MACHINE LEARNING & AI (12)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `bedrock` | **Amazon Bedrock** | `ArchitectureServiceAmazonBedrock` | LLM applications, AI agents, Content generation |
| `sagemaker` | **Amazon SageMaker** | `ArchitectureServiceAmazonSageMaker` | ML model training, Model deployment, AutoML |
| `rekognition` | **Amazon Rekognition** | `ArchitectureServiceAmazonRekognition` | Face detection, Object recognition, Content moderation |
| `comprehend` | **Amazon Comprehend** | `ArchitectureServiceAmazonComprehend` | Sentiment analysis, Entity extraction, Topic modeling |
| `lex` | **Amazon Lex** | `ArchitectureServiceAmazonLex` | Chatbots, Voice assistants, Customer service |
| `polly` | **Amazon Polly** | `ArchitectureServiceAmazonPolly` | Voice applications, Accessibility, Content narration |
| `transcribe` | **Amazon Transcribe** | `ArchitectureServiceAmazonTranscribe` | Transcription, Subtitles, Call analytics |
| `translate` | **Amazon Translate** | `ArchitectureServiceAmazonTranslate` | Content localization, Real-time translation, Multilingual apps |
| `textract` | **Amazon Textract** | `ArchitectureServiceAmazonTextract` | Document processing, Form extraction, OCR |
| `forecast` | **Amazon Forecast** | `ArchitectureServiceAmazonForecast` | Demand forecasting, Resource planning, Financial planning |
| `personalize` | **Amazon Personalize** | `ArchitectureServiceAmazonPersonalize` | Product recommendations, Content personalization, Marketing |
| `kendra` | **Amazon Kendra** | `ArchitectureServiceAmazonKendra` | Enterprise search, Document search, Knowledge bases |

### 7. ANALYTICS (10)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `athena` | **Amazon Athena** | `ArchitectureServiceAmazonAthena` | Log analysis, Data exploration, Ad-hoc queries |
| `emr` | **Amazon EMR** | `ArchitectureServiceAmazonEMR` | Big data processing, Machine learning, Data transformation |
| `kinesis` | **Amazon Kinesis** | `ArchitectureServiceAmazonKinesis` | Real-time analytics, Log processing, IoT data |
| `redshift` | **Amazon Redshift** | `ArchitectureServiceAmazonRedshift` | Business intelligence, Data warehousing, Analytics |
| `quicksight` | **Amazon QuickSight** | `ArchitectureServiceAmazonQuickSight` | Dashboards, Data visualization, Business analytics |
| `glue` | **AWS Glue** | `ArchitectureServiceAWSGlue` | Data preparation, ETL jobs, Data catalog |
| `data-pipeline` | **AWS Data Pipeline** | `ArchitectureServiceAWSDataPipeline` | Data movement, Workflow automation, Data processing |
| `lake-formation` | **AWS Lake Formation** | `ArchitectureServiceAWSLakeFormation` | Data lakes, Data governance, Access control |
| `msk` | **Amazon MSK** | `ArchitectureServiceAmazonManagedStreamingforApacheKafka` | Event streaming, Log aggregation, Real-time analytics |
| `opensearch` | **Amazon OpenSearch** | `ArchitectureServiceAmazonOpenSearchService` | Log analytics, Full-text search, Application monitoring |

### 8. APPLICATION INTEGRATION (7)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `eventbridge` | **Amazon EventBridge** | `ArchitectureServiceAmazonEventBridge` | Event-driven architecture, Application integration, Scheduled events |
| `sqs` | **Amazon SQS** | `ArchitectureServiceAmazonSimpleQueueService` | Decoupling, Asynchronous processing, Buffering |
| `sns` | **Amazon SNS** | `ArchitectureServiceAmazonSimpleNotificationService` | Notifications, Fan-out, Mobile push |
| `step-functions` | **AWS Step Functions** | `ArchitectureServiceAWSStepFunctions` | Workflow automation, Microservices orchestration, ETL pipelines |
| `appflow` | **Amazon AppFlow** | `ArchitectureServiceAmazonAppFlow` | Data integration, SaaS connectors, Data transfer |
| `mq` | **Amazon MQ** | `ArchitectureServiceAmazonMQ` | Message brokering, Legacy app integration, ActiveMQ/RabbitMQ |
| `appsync` | **AWS AppSync** | `ArchitectureServiceAWSAppSync` | GraphQL APIs, Real-time data, Offline sync |

### 9. MANAGEMENT & GOVERNANCE (10)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `cloudwatch` | **Amazon CloudWatch** | `ArchitectureServiceAmazonCloudWatch` | Metrics, Logs, Alarms, Dashboards |
| `cloudformation` | **AWS CloudFormation** | `ArchitectureServiceAWSCloudFormation` | Resource provisioning, Infrastructure automation, Stack management |
| `cloudtrail` | **AWS CloudTrail** | `ArchitectureServiceAWSCloudTrail` | Audit logging, Compliance, Security analysis |
| `config` | **AWS Config** | `ArchitectureServiceAWSConfig` | Compliance auditing, Resource tracking, Change management |
| `systems-manager` | **AWS Systems Manager** | `ArchitectureServiceAWSSystemsManager` | Patch management, Configuration management, Automation |
| `organizations` | **AWS Organizations** | `ArchitectureServiceAWSOrganizations` | Account management, Billing consolidation, Policy management |
| `control-tower` | **AWS Control Tower** | `ArchitectureServiceAWSControlTower` | Landing zone, Account governance, Compliance |
| `service-catalog` | **AWS Service Catalog** | `ArchitectureServiceAWSServiceCatalog` | Self-service portal, Standardized deployments, Governance |
| `trusted-advisor` | **AWS Trusted Advisor** | `ArchitectureServiceAWSTrustedAdvisor` | Cost optimization, Security, Performance, Fault tolerance |
| `well-architected-tool` | **AWS Well-Architected Tool** | `ArchitectureServiceAWSWellArchitectedTool` | Architecture review, Best practices, Risk assessment |

### 10. DEVELOPER TOOLS (7)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `codecommit` | **AWS CodeCommit** | `ArchitectureServiceAWSCodeCommit` | Git repositories, Version control, Code collaboration |
| `codebuild` | **AWS CodeBuild** | `ArchitectureServiceAWSCodeBuild` | CI/CD, Build automation, Testing |
| `codedeploy` | **AWS CodeDeploy** | `ArchitectureServiceAWSCodeDeploy` | Deployment automation, Blue/green deployments, Rolling updates |
| `codepipeline` | **AWS CodePipeline** | `ArchitectureServiceAWSCodePipeline` | CI/CD pipelines, Release automation, Workflow orchestration |
| `xray` | **AWS X-Ray** | `ArchitectureServiceAWSXRay` | Distributed tracing, Performance analysis, Debugging |
| `cloud9` | **AWS Cloud9** | `ArchitectureServiceAWSCloud9` | Code editing, Debugging, Collaboration |
| `cloudshell` | **AWS CloudShell** | `ArchitectureServiceAWSCloudShell` | CLI access, Scripting, Quick tasks |

### 11. MIGRATION & TRANSFER (5)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `migration-hub` | **AWS Migration Hub** | `ArchitectureServiceAWSMigrationHub` | Migration tracking, Application discovery, Migration planning |
| `application-migration` | **AWS Application Migration Service** | `ArchitectureServiceAWSApplicationMigrationService` | Server migration, Rehosting, Disaster recovery |
| `datasync` | **AWS DataSync** | `ArchitectureServiceAWSDataSync` | Data migration, Data replication, Data archiving |
| `transfer-family` | **AWS Transfer Family** | `ArchitectureServiceAWSTransferFamily` | SFTP, FTPS, FTP, File transfers |
| `snow-family` | **AWS Snow Family** | `ArchitectureServiceAWSSnowFamily` | Large data migration, Edge computing, Offline data transfer |

### 12. FRONT-END WEB & MOBILE (3)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `amplify` | **AWS Amplify** | `ArchitectureServiceAWSAmplify` | Web hosting, Mobile backends, CI/CD for front-end |
| `app-runner` | **AWS App Runner** | `ArchitectureServiceAWSAppRunner` | Web applications, APIs, Microservices |
| `device-farm` | **AWS Device Farm** | `ArchitectureServiceAWSDeviceFarm` | Mobile testing, Cross-device testing, Automated testing |

### 13. MEDIA SERVICES (5)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `elastic-transcoder` | **Amazon Elastic Transcoder** | `ArchitectureServiceAmazonElasticTranscoder` | Video transcoding, Format conversion, Media processing |
| `mediaconvert` | **AWS Elemental MediaConvert** | `ArchitectureServiceAWSElementalMediaConvert` | VOD workflows, Broadcast, OTT content |
| `medialive` | **AWS Elemental MediaLive** | `ArchitectureServiceAWSElementalMediaLive` | Live streaming, Broadcast, Live events |
| `mediapackage` | **AWS Elemental MediaPackage** | `ArchitectureServiceAWSElementalMediaPackage` | Video delivery, Content protection, Multi-format delivery |
| `mediastore` | **AWS Elemental MediaStore** | `ArchitectureServiceAWSElementalMediaStore` | Live video storage, Low-latency delivery, Media origin |

### 14. IOT (4)

| ID | Official Name | Icon Component | Use Cases |
|----|--------------|----------------|-----------|
| `iot-core` | **AWS IoT Core** | `ArchitectureServiceAWSIoTCore` | Device connectivity, Message routing, Device shadows |
| `iot-greengrass` | **AWS IoT Greengrass** | `ArchitectureServiceAWSIoTGreengrass` | Edge computing, Local processing, Offline operation |
| `iot-analytics` | **AWS IoT Analytics** | `ArchitectureServiceAWSIoTAnalytics` | IoT data analysis, Time-series analytics, Device insights |
| `iot-events` | **AWS IoT Events** | `ArchitectureServiceAWSIoTEvents` | Event detection, Anomaly detection, Automated responses |

---

## Usage Examples

### Import Individual Service

```typescript
import { awsServiceRegistry, getService } from '@/components/AWSServiceIconRegistry'

// Get service by ID
const lambda = getService('lambda')
console.log(lambda?.officialName) // "AWS Lambda"

// Render icon
const LambdaIcon = lambda?.icon
return <LambdaIcon size={48} />
```

### Get Services by Category

```typescript
import { getServicesByCategory } from '@/components/AWSServiceIconRegistry'

const computeServices = getServicesByCategory('Compute')
// Returns array of 8 compute services
```

### Search Services

```typescript
import { searchServices } from '@/components/AWSServiceIconRegistry'

const results = searchServices('database')
// Returns all database-related services
```

### List All Categories

```typescript
import { getAllCategories, getTotalServiceCount } from '@/components/AWSServiceIconRegistry'

const categories = getAllCategories()
// Returns: ['Compute', 'Storage', 'Database', ...]

const total = getTotalServiceCount()
// Returns: 100+
```

---

## Architecture Diagram Integration

All services in this registry are ready to use in AWS architecture diagrams:

```typescript
import { awsServiceRegistry } from '@/components/AWSServiceIconRegistry'
import type { ServiceNode } from '@/components/AWSArchitectureDiagram'

const services: ServiceNode[] = [
  {
    id: 'lambda-1',
    name: awsServiceRegistry.lambda.officialName, // "AWS Lambda"
    type: 'aws',
    icon: awsServiceRegistry.lambda.icon,
    description: 'Process API requests',
    x: 100,
    y: 100
  },
  {
    id: 'dynamodb-1',
    name: awsServiceRegistry.dynamodb.officialName, // "Amazon DynamoDB"
    type: 'aws',
    icon: awsServiceRegistry.dynamodb.icon,
    description: 'Store application data',
    x: 300,
    y: 100
  }
]
```

---

## AI Agent Guidelines

When generating AWS architectures, AI agents should:

1. **Use Official Names**: Always use `service.officialName` (e.g., "AWS Lambda", not "Lambda")
2. **Reference by ID**: Use service IDs from registry (e.g., `'lambda'`, `'dynamodb'`)
3. **Include Descriptions**: Use `service.description` for context
4. **Check Use Cases**: Match `service.useCases` to user requirements
5. **Filter by Category**: Use `getServicesByCategory()` for domain-specific services
6. **Search Semantically**: Use `searchServices()` for natural language queries

---

## Maintenance

### Adding New Services

1. Import icon from `aws-react-icons/icons/`
2. Add to appropriate category section
3. Define service in `awsServiceRegistry`
4. Add ID to `servicesByCategory`
5. Update this documentation

### Updating Service Information

Edit the service definition in `awsServiceRegistry` with:
- Official name changes
- New use cases
- Updated descriptions
- Additional tags

---

## Summary

✅ **100+ AWS Services** - Complete coverage of AWS service portfolio  
✅ **14 Categories** - Organized by service type  
✅ **Official Naming** - AWS-compliant service names  
✅ **Rich Metadata** - Descriptions, use cases, and tags  
✅ **Search & Filter** - Helper functions for service discovery  
✅ **Architecture Ready** - Direct integration with diagram components  
✅ **AI Agent Friendly** - Structured data for LLM consumption  

**Result**: A comprehensive, maintainable, and AI-friendly AWS service icon registry for building accurate architecture diagrams.
