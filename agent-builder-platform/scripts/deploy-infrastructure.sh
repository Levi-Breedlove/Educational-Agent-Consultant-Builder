#!/bin/bash

# Agent Builder Platform - Expert Consultation System Deployment Script
# This script deploys the complete AWS infrastructure for the expert consultation system

set -e  # Exit on any error

# Configuration
PROJECT_NAME="agent-builder-platform"
ENVIRONMENT="dev"
REGION="us-east-1"
STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success() {
    echo -e "${GREEN}✅ $1${NC}"
}

warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

error() {
    echo -e "${RED}❌ $1${NC}"
    exit 1
}

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites for expert consultation system deployment..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed. Please install AWS CLI v2."
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured. Run 'aws configure' first."
    fi
    
    # Check region
    CURRENT_REGION=$(aws configure get region)
    if [ "$CURRENT_REGION" != "$REGION" ]; then
        warning "Current AWS region is $CURRENT_REGION, but deployment expects $REGION"
        read -p "Continue with $REGION? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            error "Deployment cancelled. Please configure AWS CLI for $REGION region."
        fi
    fi
    
    # Check Bedrock access
    log "Verifying Bedrock access for AI consultants..."
    if ! aws bedrock list-foundation-models --region $REGION &> /dev/null; then
        warning "Cannot access Bedrock service. This is required for AI consultants."
        warning "Make sure Bedrock is available in your region and you have proper permissions."
    fi
    
    # Get AWS Account ID
    AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
    log "Deploying to AWS Account: $AWS_ACCOUNT_ID"
    
    success "Prerequisites check completed"
}

# Validate CloudFormation template
validate_template() {
    log "Validating CloudFormation template..."
    
    if aws cloudformation validate-template \
        --template-body file://infrastructure/main-stack.yaml \
        --region $REGION > /dev/null; then
        success "CloudFormation template is valid"
    else
        error "CloudFormation template validation failed"
    fi
}

# Deploy infrastructure
deploy_infrastructure() {
    log "Deploying expert consultation system infrastructure..."
    
    # Check if stack exists
    if aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION &> /dev/null; then
        
        log "Stack exists, updating..."
        aws cloudformation update-stack \
            --stack-name $STACK_NAME \
            --template-body file://infrastructure/main-stack.yaml \
            --parameters ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
                        ParameterKey=ProjectName,ParameterValue=$PROJECT_NAME \
            --capabilities CAPABILITY_NAMED_IAM \
            --region $REGION
        
        log "Waiting for stack update to complete..."
        aws cloudformation wait stack-update-complete \
            --stack-name $STACK_NAME \
            --region $REGION
    else
        log "Creating new stack..."
        aws cloudformation create-stack \
            --stack-name $STACK_NAME \
            --template-body file://infrastructure/main-stack.yaml \
            --parameters ParameterKey=Environment,ParameterValue=$ENVIRONMENT \
                        ParameterKey=ProjectName,ParameterValue=$PROJECT_NAME \
            --capabilities CAPABILITY_NAMED_IAM \
            --region $REGION \
            --tags Key=Project,Value="Expert Consultation System" \
                   Key=Environment,Value=$ENVIRONMENT \
                   Key=Purpose,Value="AWS Agent Hackathon"
        
        log "Waiting for stack creation to complete..."
        aws cloudformation wait stack-create-complete \
            --stack-name $STACK_NAME \
            --region $REGION
    fi
    
    success "Infrastructure deployment completed"
}

# Get stack outputs
get_stack_outputs() {
    log "Retrieving stack outputs..."
    
    # Get all outputs
    OUTPUTS=$(aws cloudformation describe-stacks \
        --stack-name $STACK_NAME \
        --region $REGION \
        --query 'Stacks[0].Outputs' \
        --output json)
    
    # Extract key values
    PROJECT_BUCKET=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="ProjectStorageBucket") | .OutputValue')
    AGENTS_BUCKET=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="GeneratedAgentsBucket") | .OutputValue')
    KNOWLEDGE_BUCKET=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="KnowledgeBaseBucket") | .OutputValue')
    ECS_CLUSTER=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="ECSCluster") | .OutputValue')
    LOAD_BALANCER_DNS=$(echo $OUTPUTS | jq -r '.[] | select(.OutputKey=="LoadBalancerDNS") | .OutputValue')
    
    # Save outputs to file for other scripts
    cat > .env << EOF
# Expert Consultation System Environment Variables
AWS_REGION=$REGION
AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID
PROJECT_NAME=$PROJECT_NAME
ENVIRONMENT=$ENVIRONMENT
STACK_NAME=$STACK_NAME

# S3 Buckets
PROJECT_STORAGE_BUCKET=$PROJECT_BUCKET
GENERATED_AGENTS_BUCKET=$AGENTS_BUCKET
KNOWLEDGE_BASE_BUCKET=$KNOWLEDGE_BUCKET

# ECS Configuration
ECS_CLUSTER=$ECS_CLUSTER

# Load Balancer
LOAD_BALANCER_DNS=$LOAD_BALANCER_DNS

# DynamoDB Tables
PROJECTS_TABLE=${PROJECT_NAME}-projects-${ENVIRONMENT}
CONFIGS_TABLE=${PROJECT_NAME}-configs-${ENVIRONMENT}
AWS_KNOWLEDGE_TABLE=${PROJECT_NAME}-aws-knowledge-${ENVIRONMENT}
STRANDS_KNOWLEDGE_TABLE=${PROJECT_NAME}-strands-knowledge-${ENVIRONMENT}
MCP_REPOSITORY_TABLE=${PROJECT_NAME}-mcp-repository-${ENVIRONMENT}
EOF
    
    success "Stack outputs saved to .env file"
}

# Set up cost monitoring
setup_cost_monitoring() {
    log "Setting up cost monitoring and billing alerts..."
    
    # Create billing alarm for $15 threshold
    aws cloudwatch put-metric-alarm \
        --alarm-name "${PROJECT_NAME}-cost-warning" \
        --alarm-description "Warning when costs exceed $15" \
        --metric-name EstimatedCharges \
        --namespace AWS/Billing \
        --statistic Maximum \
        --period 86400 \
        --threshold 15 \
        --comparison-operator GreaterThanThreshold \
        --dimensions Name=Currency,Value=USD \
        --evaluation-periods 1 \
        --region us-east-1  # Billing metrics are only in us-east-1
    
    # Create billing alarm for $20 threshold
    aws cloudwatch put-metric-alarm \
        --alarm-name "${PROJECT_NAME}-cost-critical" \
        --alarm-description "Critical alert when costs exceed $20" \
        --metric-name EstimatedCharges \
        --namespace AWS/Billing \
        --statistic Maximum \
        --period 86400 \
        --threshold 20 \
        --comparison-operator GreaterThanThreshold \
        --dimensions Name=Currency,Value=USD \
        --evaluation-periods 1 \
        --region us-east-1
    
    success "Cost monitoring configured"
}

# Verify deployment
verify_deployment() {
    log "Verifying expert consultation system deployment..."
    
    # Check S3 buckets
    if aws s3 ls s3://$PROJECT_BUCKET &> /dev/null; then
        success "Project storage bucket accessible"
    else
        error "Project storage bucket not accessible"
    fi
    
    # Check DynamoDB tables
    if aws dynamodb describe-table --table-name $PROJECTS_TABLE --region $REGION &> /dev/null; then
        success "DynamoDB tables created successfully"
    else
        error "DynamoDB tables not accessible"
    fi
    
    # Check ECS cluster
    if aws ecs describe-clusters --clusters $ECS_CLUSTER --region $REGION &> /dev/null; then
        success "ECS cluster created successfully"
    else
        error "ECS cluster not accessible"
    fi
    
    success "Deployment verification completed"
}

# Display deployment summary
display_summary() {
    echo
    echo "🎉 Expert Consultation System Infrastructure Deployed Successfully!"
    echo
    echo "📊 Deployment Summary:"
    echo "  • Project: $PROJECT_NAME"
    echo "  • Environment: $ENVIRONMENT"
    echo "  • Region: $REGION"
    echo "  • Stack: $STACK_NAME"
    echo
    echo "🔗 Key Resources:"
    echo "  • Load Balancer: http://$LOAD_BALANCER_DNS"
    echo "  • ECS Cluster: $ECS_CLUSTER"
    echo "  • Project Bucket: $PROJECT_BUCKET"
    echo "  • Agents Bucket: $AGENTS_BUCKET"
    echo
    echo "💰 Cost Monitoring:"
    echo "  • Warning Alert: $15 threshold"
    echo "  • Critical Alert: $20 threshold"
    echo "  • Estimated Monthly Cost: $10-20"
    echo
    echo "🚀 Next Steps:"
    echo "  1. Run './scripts/setup-agent-core.sh' to configure AI consultants"
    echo "  2. Run './scripts/deploy-expert-system.sh' to deploy the application"
    echo "  3. Access the platform at http://$LOAD_BALANCER_DNS once deployed"
    echo
    echo "📝 Configuration saved to .env file"
    echo
}

# Main execution
main() {
    echo "🚀 Agent Builder Platform - Expert Consultation System Deployment"
    echo "=================================================================="
    echo
    
    check_prerequisites
    validate_template
    deploy_infrastructure
    get_stack_outputs
    setup_cost_monitoring
    verify_deployment
    display_summary
    
    echo "✅ Infrastructure deployment completed successfully!"
}

# Run main function
main "$@"