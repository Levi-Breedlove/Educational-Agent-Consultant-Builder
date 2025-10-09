import ArchitectureServiceAmazonAPIGateway from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonAPIGateway'
import ArchitectureServiceAWSLambda from 'aws-react-icons/lib/icons/ArchitectureServiceAWSLambda'
import ArchitectureServiceAmazonDynamoDB from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonDynamoDB'
import ArchitectureServiceAmazonSimpleStorageService from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonSimpleStorageService'
import ArchitectureServiceAmazonCloudWatch from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonCloudWatch'
import ArchitectureServiceAmazonElasticContainerService from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonElasticContainerService'
import ArchitectureServiceElasticLoadBalancing from 'aws-react-icons/lib/icons/ArchitectureServiceElasticLoadBalancing'
import ArchitectureServiceAmazonRDS from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonRDS'
import ArchitectureServiceAmazonEventBridge from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonEventBridge'
import ArchitectureServiceAmazonSimpleQueueService from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonSimpleQueueService'
import ArchitectureServiceAmazonBedrock from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonBedrock'
import ArchitectureServiceAmazonOpenSearchService from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonOpenSearchService'
import ArchitectureServiceAWSGlue from 'aws-react-icons/lib/icons/ArchitectureServiceAWSGlue'
import ArchitectureServiceAmazonAthena from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonAthena'
import ArchitectureServiceAmazonQuickSight from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonQuickSight'
import ArchitectureServiceAWSIdentityandAccessManagement from 'aws-react-icons/lib/icons/ArchitectureServiceAWSIdentityandAccessManagement'
import ArchitectureGroupVirtualprivatecloudVPC from 'aws-react-icons/lib/icons/ArchitectureGroupVirtualprivatecloudVPC'
import ArchitectureServiceAmazonSimpleNotificationService from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonSimpleNotificationService'

// Additional icons for expanded templates
import ArchitectureServiceAmazonCognito from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonCognito'
import ArchitectureServiceAmazonKinesis from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonKinesis'
import ArchitectureServiceAmazonRedshift from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonRedshift'
import ArchitectureServiceAWSStepFunctions from 'aws-react-icons/lib/icons/ArchitectureServiceAWSStepFunctions'
import ArchitectureServiceAmazonElastiCache from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonElastiCache'
import ArchitectureServiceAmazonCloudFront from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonCloudFront'
import ArchitectureServiceAmazonRoute53 from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonRoute53'
import ArchitectureServiceAWSWAF from 'aws-react-icons/lib/icons/ArchitectureServiceAWSWAF'
import ArchitectureServiceAmazonSageMaker from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonSageMaker'
import ArchitectureServiceAWSCodePipeline from 'aws-react-icons/lib/icons/ArchitectureServiceAWSCodePipeline'
import ArchitectureServiceAWSCodeBuild from 'aws-react-icons/lib/icons/ArchitectureServiceAWSCodeBuild'
import ArchitectureServiceAWSCodeDeploy from 'aws-react-icons/lib/icons/ArchitectureServiceAWSCodeDeploy'
import ArchitectureServiceAmazonEMR from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonEMR'
import ArchitectureServiceAWSSecretsManager from 'aws-react-icons/lib/icons/ArchitectureServiceAWSSecretsManager'
import ArchitectureServiceAmazonConnect from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonConnect'
import ArchitectureServiceAmazonLex from 'aws-react-icons/lib/icons/ArchitectureServiceAmazonLex'

// Generic resource icons (for non-AWS entities)
import ResourceUser from 'aws-react-icons/lib/icons/ResourceUser'
import ResourceClient from 'aws-react-icons/lib/icons/ResourceClient'

// Create shorter aliases for easier use
const ApiGatewayIcon = ArchitectureServiceAmazonAPIGateway
const LambdaIcon = ArchitectureServiceAWSLambda
const DynamoDbIcon = ArchitectureServiceAmazonDynamoDB
const S3Icon = ArchitectureServiceAmazonSimpleStorageService
const CloudWatchIcon = ArchitectureServiceAmazonCloudWatch
const EcsIcon = ArchitectureServiceAmazonElasticContainerService
const AlbIcon = ArchitectureServiceElasticLoadBalancing
const RdsIcon = ArchitectureServiceAmazonRDS
const EventBridgeIcon = ArchitectureServiceAmazonEventBridge
const SqsIcon = ArchitectureServiceAmazonSimpleQueueService
const BedrockIcon = ArchitectureServiceAmazonBedrock
const OpenSearchServiceIcon = ArchitectureServiceAmazonOpenSearchService
const GlueIcon = ArchitectureServiceAWSGlue
const AthenaIcon = ArchitectureServiceAmazonAthena
const QuickSightIcon = ArchitectureServiceAmazonQuickSight
const IamIcon = ArchitectureServiceAWSIdentityandAccessManagement
const VpcIcon = ArchitectureGroupVirtualprivatecloudVPC
const SnsIcon = ArchitectureServiceAmazonSimpleNotificationService
const CognitoIcon = ArchitectureServiceAmazonCognito
const KinesisIcon = ArchitectureServiceAmazonKinesis
const RedshiftIcon = ArchitectureServiceAmazonRedshift
const StepFunctionsIcon = ArchitectureServiceAWSStepFunctions
const ElastiCacheIcon = ArchitectureServiceAmazonElastiCache
const CloudFrontIcon = ArchitectureServiceAmazonCloudFront
const Route53Icon = ArchitectureServiceAmazonRoute53
const WAFIcon = ArchitectureServiceAWSWAF
const SageMakerIcon = ArchitectureServiceAmazonSageMaker
const CodePipelineIcon = ArchitectureServiceAWSCodePipeline
const CodeBuildIcon = ArchitectureServiceAWSCodeBuild
const CodeDeployIcon = ArchitectureServiceAWSCodeDeploy
const EMRIcon = ArchitectureServiceAmazonEMR
const SecretsManagerIcon = ArchitectureServiceAWSSecretsManager
const ConnectIcon = ArchitectureServiceAmazonConnect
const LexIcon = ArchitectureServiceAmazonLex
const UserIcon = ResourceUser
const ClientIcon = ResourceClient

import type { ServiceNode, Connection } from './AWSArchitectureDiagram'

export interface AWSArchitectureTemplate {
  id: string
  name: string
  description: string
  category: string
  tags: string[]
  services: ServiceNode[]
  connections: Connection[]
}

// Professional AWS Architecture Templates with actual AWS icons
export const awsArchitectureTemplates: AWSArchitectureTemplate[] = [
  {
    id: 'serverless-api',
    name: 'Serverless REST API',
    description: 'API Gateway + Lambda + DynamoDB pattern for serverless REST APIs with CloudWatch monitoring',
    category: 'Serverless',
    tags: ['API Gateway', 'Lambda', 'DynamoDB', 'CloudWatch'],
    services: [
      { id: 'client', name: 'Client', type: 'aws', icon: ClientIcon, description: 'Web/Mobile Client', x: 50, y: 200 },
      { id: 'apigw', name: 'Amazon API Gateway', type: 'aws', icon: ApiGatewayIcon, description: 'REST API endpoint', x: 220, y: 200 },
      { id: 'lambda', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Business logic', x: 390, y: 200 },
      { id: 'dynamodb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, description: 'NoSQL database', x: 560, y: 60 },
      { id: 's3', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Object storage', x: 560, y: 340 },
      { id: 'cloudwatch', name: 'Amazon CloudWatch', type: 'aws', icon: CloudWatchIcon, description: 'Monitoring & logs', x: 390, y: 340 },
      { id: 'iam', name: 'AWS IAM', type: 'aws', icon: IamIcon, description: 'Access control', x: 390, y: 60 },
    ],
    connections: [
      { from: 'client', to: 'apigw', label: 'HTTPS' },
      { from: 'apigw', to: 'lambda', label: 'invoke' },
      { from: 'lambda', to: 'dynamodb', label: 'read/write' },
      { from: 'lambda', to: 's3', label: 'store' },
      { from: 'lambda', to: 'cloudwatch', label: 'logs', dashed: true },
      { from: 'iam', to: 'lambda', label: 'authorize', dashed: true },
    ],
  },
  {
    id: 'ecs-fargate',
    name: 'ECS Fargate Application',
    description: 'Containerized application with ECS Fargate, Application Load Balancer, and RDS database',
    category: 'Containers',
    tags: ['ECS', 'Fargate', 'ALB', 'RDS', 'VPC'],
    services: [
      { id: 'user', name: 'User', type: 'aws', icon: UserIcon, description: 'End User', x: 50, y: 200 },
      { id: 'alb', name: 'Elastic Load Balancing', type: 'aws', icon: AlbIcon, description: 'Application Load Balancer', x: 220, y: 200 },
      { id: 'ecs', name: 'Amazon ECS Fargate', type: 'aws', icon: EcsIcon, description: 'Container service', x: 390, y: 200 },
      { id: 'rds', name: 'Amazon RDS', type: 'aws', icon: RdsIcon, description: 'Relational database', x: 560, y: 60 },
      { id: 's3', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Static assets', x: 560, y: 340 },
      { id: 'cloudwatch', name: 'Amazon CloudWatch', type: 'aws', icon: CloudWatchIcon, description: 'Monitoring', x: 390, y: 340 },
      { id: 'vpc', name: 'Amazon VPC', type: 'aws', icon: VpcIcon, description: 'Network isolation', x: 390, y: 60 },
    ],
    connections: [
      { from: 'user', to: 'alb', label: 'HTTPS' },
      { from: 'alb', to: 'ecs', label: 'route' },
      { from: 'ecs', to: 'rds', label: 'query' },
      { from: 'ecs', to: 's3', label: 'read' },
      { from: 'ecs', to: 'cloudwatch', label: 'metrics', dashed: true },
      { from: 'vpc', to: 'ecs', label: 'isolate', dashed: true },
      { from: 'vpc', to: 'rds', label: 'secure', dashed: true },
    ],
  },
  {
    id: 'event-driven',
    name: 'Event-Driven Architecture',
    description: 'EventBridge + Lambda + SQS for scalable event-driven processing with dead-letter queues',
    category: 'Event-Driven',
    tags: ['EventBridge', 'Lambda', 'SQS', 'DynamoDB'],
    services: [
      { id: 'source', name: 'Event Source', type: 'aws', icon: ClientIcon, description: 'External System', x: 50, y: 200 },
      { id: 'eventbridge', name: 'Amazon EventBridge', type: 'aws', icon: EventBridgeIcon, description: 'Event bus', x: 220, y: 200 },
      { id: 'lambda1', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Event processor', x: 390, y: 60 },
      { id: 'sqs', name: 'Amazon SQS', type: 'aws', icon: SqsIcon, description: 'Message queue', x: 390, y: 340 },
      { id: 'lambda2', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Queue consumer', x: 560, y: 340 },
      { id: 'dynamodb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, description: 'State storage', x: 730, y: 60 },
      { id: 's3', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Data lake', x: 730, y: 340 },
    ],
    connections: [
      { from: 'source', to: 'eventbridge', label: 'events' },
      { from: 'eventbridge', to: 'lambda1', label: 'trigger' },
      { from: 'eventbridge', to: 'sqs', label: 'enqueue' },
      { from: 'sqs', to: 'lambda2', label: 'poll' },
      { from: 'lambda1', to: 'dynamodb', label: 'write' },
      { from: 'lambda2', to: 's3', label: 'store' },
    ],
  },
  {
    id: 'ai-agent-bedrock',
    name: 'AI Agent with Bedrock',
    description: 'Amazon Bedrock + Lambda + Knowledge Base with OpenSearch for intelligent AI agents',
    category: 'AI/ML',
    tags: ['Bedrock', 'Lambda', 'OpenSearch', 'S3'],
    services: [
      { id: 'apigw', name: 'Amazon API Gateway', type: 'aws', icon: ApiGatewayIcon, description: 'API endpoint', x: 50, y: 200 },
      { id: 'lambda', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Agent orchestrator', x: 250, y: 200 },
      { id: 'bedrock', name: 'Amazon Bedrock', type: 'aws', icon: BedrockIcon, description: 'LLM inference', x: 450, y: 60 },
      { id: 'opensearch', name: 'Amazon OpenSearch', type: 'aws', icon: OpenSearchServiceIcon, description: 'Vector search', x: 450, y: 340 },
      { id: 's3', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Knowledge base', x: 650, y: 340 },
      { id: 'dynamodb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, description: 'Session state', x: 250, y: 340 },
    ],
    connections: [
      { from: 'apigw', to: 'lambda', label: 'invoke' },
      { from: 'lambda', to: 'bedrock', label: 'generate' },
      { from: 'lambda', to: 'opensearch', label: 'search' },
      { from: 's3', to: 'opensearch', label: 'index', dashed: true },
      { from: 'lambda', to: 'dynamodb', label: 'state' },
    ],
  },
  {
    id: 'data-pipeline',
    name: 'Data Analytics Pipeline',
    description: 'S3 + Glue + Athena + QuickSight for serverless data analytics and visualization',
    category: 'Analytics',
    tags: ['S3', 'Glue', 'Athena', 'QuickSight'],
    services: [
      { id: 's3raw', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Raw data', x: 50, y: 200 },
      { id: 'lambda', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'ETL trigger', x: 200, y: 200 },
      { id: 'glue', name: 'AWS Glue', type: 'aws', icon: GlueIcon, description: 'Data transformation', x: 350, y: 200 },
      { id: 's3processed', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Clean data', x: 500, y: 200 },
      { id: 'athena', name: 'Amazon Athena', type: 'aws', icon: AthenaIcon, description: 'SQL queries', x: 650, y: 60 },
      { id: 'quicksight', name: 'Amazon QuickSight', type: 'aws', icon: QuickSightIcon, description: 'Dashboards', x: 650, y: 340 },
    ],
    connections: [
      { from: 's3raw', to: 'lambda', label: 'trigger' },
      { from: 'lambda', to: 'glue', label: 'start' },
      { from: 'glue', to: 's3processed', label: 'write' },
      { from: 's3processed', to: 'athena', label: 'query' },
      { from: 'athena', to: 'quicksight', label: 'visualize' },
    ],
  },
  {
    id: 'microservices',
    name: 'Microservices Architecture',
    description: 'API Gateway routing to multiple Lambda microservices with isolated DynamoDB tables',
    category: 'Microservices',
    tags: ['API Gateway', 'Lambda', 'DynamoDB', 'SQS'],
    services: [
      { id: 'apigw', name: 'Amazon API Gateway', type: 'aws', icon: ApiGatewayIcon, description: 'API routing', x: 50, y: 250 },
      { id: 'auth', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Authentication', x: 250, y: 80 },
      { id: 'users', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'User management', x: 250, y: 220 },
      { id: 'orders', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Order processing', x: 250, y: 360 },
      { id: 'authdb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, description: 'Auth data', x: 450, y: 80 },
      { id: 'userdb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, description: 'User data', x: 450, y: 220 },
      { id: 'orderdb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, description: 'Order data', x: 450, y: 360 },
      { id: 'sqs', name: 'Amazon SQS', type: 'aws', icon: SqsIcon, description: 'Async tasks', x: 250, y: 500 },
      { id: 'notify', name: 'Amazon SNS', type: 'aws', icon: SnsIcon, description: 'Notifications', x: 450, y: 500 },
    ],
    connections: [
      { from: 'apigw', to: 'auth', label: 'auth' },
      { from: 'apigw', to: 'users', label: 'users' },
      { from: 'apigw', to: 'orders', label: 'orders' },
      { from: 'auth', to: 'authdb' },
      { from: 'users', to: 'userdb' },
      { from: 'orders', to: 'orderdb' },
      { from: 'orders', to: 'sqs', label: 'queue' },
      { from: 'sqs', to: 'notify', label: 'send' },
    ],
  },
  {
    id: 'real-time-streaming',
    name: 'Real-Time Data Streaming',
    description: 'Kinesis + Lambda + ElastiCache + Redshift for real-time data processing and analytics',
    category: 'Analytics',
    tags: ['Kinesis', 'Lambda', 'ElastiCache', 'Redshift'],
    services: [
      { id: 'source', name: 'Data Source', type: 'generic', description: 'IoT/App Events', x: 50, y: 200 },
      { id: 'kinesis', name: 'Amazon Kinesis', type: 'aws', icon: KinesisIcon, description: 'Stream processing', x: 220, y: 200 },
      { id: 'lambda', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Real-time processor', x: 390, y: 200 },
      { id: 'elasticache', name: 'Amazon ElastiCache', type: 'aws', icon: ElastiCacheIcon, description: 'Hot data cache', x: 560, y: 60 },
      { id: 'redshift', name: 'Amazon Redshift', type: 'aws', icon: RedshiftIcon, description: 'Data warehouse', x: 560, y: 340 },
      { id: 'quicksight', name: 'Amazon QuickSight', type: 'aws', icon: QuickSightIcon, description: 'Analytics dashboard', x: 730, y: 200 },
      { id: 'cloudwatch', name: 'Amazon CloudWatch', type: 'aws', icon: CloudWatchIcon, description: 'Monitoring', x: 390, y: 340 },
    ],
    connections: [
      { from: 'source', to: 'kinesis', label: 'stream' },
      { from: 'kinesis', to: 'lambda', label: 'process' },
      { from: 'lambda', to: 'elasticache', label: 'cache' },
      { from: 'lambda', to: 'redshift', label: 'store' },
      { from: 'redshift', to: 'quicksight', label: 'visualize' },
      { from: 'lambda', to: 'cloudwatch', label: 'metrics', dashed: true },
    ],
  },
  {
    id: 'ml-pipeline',
    name: 'Machine Learning Pipeline',
    description: 'SageMaker + S3 + Step Functions for end-to-end ML model training and deployment',
    category: 'AI/ML',
    tags: ['SageMaker', 'Step Functions', 'S3', 'Lambda'],
    services: [
      { id: 's3data', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Training data', x: 50, y: 200 },
      { id: 'stepfunctions', name: 'AWS Step Functions', type: 'aws', icon: StepFunctionsIcon, description: 'Workflow orchestration', x: 220, y: 200 },
      { id: 'sagemaker', name: 'Amazon SageMaker', type: 'aws', icon: SageMakerIcon, description: 'Model training', x: 390, y: 60 },
      { id: 's3model', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Model artifacts', x: 560, y: 60 },
      { id: 'lambda', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Model inference', x: 390, y: 340 },
      { id: 'apigw', name: 'Amazon API Gateway', type: 'aws', icon: ApiGatewayIcon, description: 'Inference API', x: 560, y: 340 },
      { id: 'cloudwatch', name: 'Amazon CloudWatch', type: 'aws', icon: CloudWatchIcon, description: 'Model monitoring', x: 390, y: 480 },
    ],
    connections: [
      { from: 's3data', to: 'stepfunctions', label: 'trigger' },
      { from: 'stepfunctions', to: 'sagemaker', label: 'train' },
      { from: 'sagemaker', to: 's3model', label: 'save' },
      { from: 's3model', to: 'lambda', label: 'load', dashed: true },
      { from: 'apigw', to: 'lambda', label: 'invoke' },
      { from: 'lambda', to: 'cloudwatch', label: 'metrics', dashed: true },
    ],
  },
  {
    id: 'cicd-pipeline',
    name: 'CI/CD Pipeline',
    description: 'CodePipeline + CodeBuild + CodeDeploy for automated application deployment',
    category: 'DevOps',
    tags: ['CodePipeline', 'CodeBuild', 'CodeDeploy', 'S3'],
    services: [
      { id: 'source', name: 'Source Repo', type: 'generic', description: 'Git Repository', x: 50, y: 200 },
      { id: 'codepipeline', name: 'AWS CodePipeline', type: 'aws', icon: CodePipelineIcon, description: 'CI/CD orchestration', x: 220, y: 200 },
      { id: 'codebuild', name: 'AWS CodeBuild', type: 'aws', icon: CodeBuildIcon, description: 'Build & test', x: 390, y: 60 },
      { id: 's3', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Build artifacts', x: 560, y: 60 },
      { id: 'codedeploy', name: 'AWS CodeDeploy', type: 'aws', icon: CodeDeployIcon, description: 'Deployment', x: 390, y: 340 },
      { id: 'ecs', name: 'Amazon ECS Fargate', type: 'aws', icon: EcsIcon, description: 'Target environment', x: 560, y: 340 },
      { id: 'cloudwatch', name: 'Amazon CloudWatch', type: 'aws', icon: CloudWatchIcon, description: 'Pipeline monitoring', x: 390, y: 480 },
    ],
    connections: [
      { from: 'source', to: 'codepipeline', label: 'commit' },
      { from: 'codepipeline', to: 'codebuild', label: 'build' },
      { from: 'codebuild', to: 's3', label: 'store' },
      { from: 's3', to: 'codedeploy', label: 'deploy' },
      { from: 'codedeploy', to: 'ecs', label: 'update' },
      { from: 'codepipeline', to: 'cloudwatch', label: 'logs', dashed: true },
    ],
  },
  {
    id: 'secure-web-app',
    name: 'Secure Web Application',
    description: 'CloudFront + WAF + Cognito + Secrets Manager for secure, scalable web applications',
    category: 'Security',
    tags: ['CloudFront', 'WAF', 'Cognito', 'Secrets Manager'],
    services: [
      { id: 'user', name: 'User', type: 'generic', description: 'End User', x: 50, y: 200 },
      { id: 'route53', name: 'Amazon Route 53', type: 'aws', icon: Route53Icon, description: 'DNS routing', x: 150, y: 200 },
      { id: 'cloudfront', name: 'Amazon CloudFront', type: 'aws', icon: CloudFrontIcon, description: 'CDN', x: 270, y: 200 },
      { id: 'waf', name: 'AWS WAF', type: 'aws', icon: WAFIcon, description: 'Web firewall', x: 270, y: 60 },
      { id: 'alb', name: 'Elastic Load Balancing', type: 'aws', icon: AlbIcon, description: 'Load balancer', x: 420, y: 200 },
      { id: 'cognito', name: 'Amazon Cognito', type: 'aws', icon: CognitoIcon, description: 'User authentication', x: 570, y: 60 },
      { id: 'ecs', name: 'Amazon ECS Fargate', type: 'aws', icon: EcsIcon, description: 'Application', x: 570, y: 200 },
      { id: 'secrets', name: 'AWS Secrets Manager', type: 'aws', icon: SecretsManagerIcon, description: 'Credentials', x: 720, y: 200 },
      { id: 'rds', name: 'Amazon RDS', type: 'aws', icon: RdsIcon, description: 'Database', x: 570, y: 340 },
    ],
    connections: [
      { from: 'user', to: 'route53', label: 'DNS' },
      { from: 'route53', to: 'cloudfront', label: 'resolve' },
      { from: 'waf', to: 'cloudfront', label: 'protect', dashed: true },
      { from: 'cloudfront', to: 'alb', label: 'forward' },
      { from: 'alb', to: 'ecs', label: 'route' },
      { from: 'ecs', to: 'cognito', label: 'auth' },
      { from: 'ecs', to: 'secrets', label: 'retrieve' },
      { from: 'ecs', to: 'rds', label: 'query' },
    ],
  },
  {
    id: 'big-data-processing',
    name: 'Big Data Processing',
    description: 'EMR + S3 + Glue + Athena for large-scale data processing and analytics',
    category: 'Analytics',
    tags: ['EMR', 'S3', 'Glue', 'Athena'],
    services: [
      { id: 's3raw', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Raw data lake', x: 50, y: 200 },
      { id: 'glue', name: 'AWS Glue', type: 'aws', icon: GlueIcon, description: 'Data catalog', x: 200, y: 60 },
      { id: 'emr', name: 'Amazon EMR', type: 'aws', icon: EMRIcon, description: 'Spark processing', x: 350, y: 200 },
      { id: 's3processed', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Processed data', x: 500, y: 200 },
      { id: 'athena', name: 'Amazon Athena', type: 'aws', icon: AthenaIcon, description: 'SQL analytics', x: 650, y: 60 },
      { id: 'quicksight', name: 'Amazon QuickSight', type: 'aws', icon: QuickSightIcon, description: 'Visualization', x: 650, y: 340 },
      { id: 'cloudwatch', name: 'Amazon CloudWatch', type: 'aws', icon: CloudWatchIcon, description: 'Job monitoring', x: 350, y: 340 },
    ],
    connections: [
      { from: 's3raw', to: 'glue', label: 'catalog' },
      { from: 'glue', to: 'emr', label: 'metadata' },
      { from: 's3raw', to: 'emr', label: 'read' },
      { from: 'emr', to: 's3processed', label: 'write' },
      { from: 's3processed', to: 'athena', label: 'query' },
      { from: 'athena', to: 'quicksight', label: 'visualize' },
      { from: 'emr', to: 'cloudwatch', label: 'metrics', dashed: true },
    ],
  },
  {
    id: 'contact-center',
    name: 'AI-Powered Contact Center',
    description: 'Amazon Connect + Lex + Lambda for intelligent customer service automation',
    category: 'AI/ML',
    tags: ['Connect', 'Lex', 'Lambda', 'DynamoDB'],
    services: [
      { id: 'customer', name: 'Customer', type: 'generic', description: 'Phone/Web', x: 50, y: 200 },
      { id: 'connect', name: 'Amazon Connect', type: 'aws', icon: ConnectIcon, description: 'Contact center', x: 220, y: 200 },
      { id: 'lex', name: 'Amazon Lex', type: 'aws', icon: LexIcon, description: 'Conversational AI', x: 390, y: 60 },
      { id: 'lambda', name: 'AWS Lambda', type: 'aws', icon: LambdaIcon, description: 'Business logic', x: 560, y: 60 },
      { id: 'dynamodb', name: 'Amazon DynamoDB', type: 'aws', icon: DynamoDbIcon, description: 'Customer data', x: 730, y: 60 },
      { id: 's3', name: 'Amazon S3', type: 'aws', icon: S3Icon, description: 'Call recordings', x: 390, y: 340 },
      { id: 'cloudwatch', name: 'Amazon CloudWatch', type: 'aws', icon: CloudWatchIcon, description: 'Analytics', x: 560, y: 340 },
    ],
    connections: [
      { from: 'customer', to: 'connect', label: 'call/chat' },
      { from: 'connect', to: 'lex', label: 'interact' },
      { from: 'lex', to: 'lambda', label: 'fulfill' },
      { from: 'lambda', to: 'dynamodb', label: 'query' },
      { from: 'connect', to: 's3', label: 'record' },
      { from: 'connect', to: 'cloudwatch', label: 'metrics', dashed: true },
    ],
  },
]
