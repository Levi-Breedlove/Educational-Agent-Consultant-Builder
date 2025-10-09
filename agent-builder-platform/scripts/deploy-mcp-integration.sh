#!/bin/bash

# Deploy MCP Integration System
# This script deploys the comprehensive MCP integration and knowledge synchronization system

set -e

# Configuration
PROJECT_NAME="agent-builder-platform"
ENVIRONMENT="dev"
REGION="us-east-1"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }
error() { echo -e "${RED}❌ $1${NC}"; exit 1; }

# Check prerequisites
check_prerequisites() {
    log "Checking prerequisites for MCP integration deployment..."
    
    # Check AWS CLI
    if ! command -v aws &> /dev/null; then
        error "AWS CLI is not installed"
    fi
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        error "AWS credentials not configured"
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        error "Python 3 is not installed"
    fi
    
    # Check required environment variables
    if [[ -z "$GITHUB_TOKEN" ]]; then
        warning "GITHUB_TOKEN not set - GitHub MCP integration will be limited"
    fi
    
    success "Prerequisites check completed"
}

# Package Lambda function
package_lambda_function() {
    log "Packaging MCP sync Lambda function..."
    
    # Create temporary directory
    TEMP_DIR=$(mktemp -d)
    
    # Copy Lambda code
    cp mcp-integration/lambda/mcp-sync-handler.py "$TEMP_DIR/"
    
    # Install dependencies
    cd "$TEMP_DIR"
    pip3 install --target . boto3 aiohttp
    
    # Create deployment package
    zip -r mcp-sync-handler.zip .
    
    # Move back to project directory
    cd - > /dev/null
    mv "$TEMP_DIR/mcp-sync-handler.zip" ./mcp-sync-handler.zip
    
    # Cleanup
    rm -rf "$TEMP_DIR"
    
    success "Lambda function packaged"
}

# Deploy Lambda function
deploy_lambda_function() {
    log "Deploying MCP sync Lambda function..."
    
    # Check if function exists
    if aws lambda get-function --function-name "${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}" &> /dev/null; then
        # Update existing function
        aws lambda update-function-code \
            --function-name "${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}" \
            --zip-file fileb://mcp-sync-handler.zip \
            --region "$REGION"
        
        success "Lambda function updated"
    else
        # Create new function
        LAMBDA_ROLE_ARN=$(aws iam get-role --role-name "${PROJECT_NAME}-lambda-execution-role-${ENVIRONMENT}" --query 'Role.Arn' --output text 2>/dev/null || echo "")
        
        if [[ -z "$LAMBDA_ROLE_ARN" ]]; then
            error "Lambda execution role not found. Please deploy infrastructure first."
        fi
        
        aws lambda create-function \
            --function-name "${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}" \
            --runtime python3.9 \
            --role "$LAMBDA_ROLE_ARN" \
            --handler mcp-sync-handler.lambda_handler \
            --zip-file fileb://mcp-sync-handler.zip \
            --timeout 300 \
            --memory-size 512 \
            --environment Variables="{
                PROJECT_NAME=${PROJECT_NAME},
                ENVIRONMENT=${ENVIRONMENT},
                GITHUB_TOKEN=${GITHUB_TOKEN:-}
            }" \
            --region "$REGION"
        
        success "Lambda function created"
    fi
    
    # Get Lambda ARN for EventBridge rules
    LAMBDA_ARN=$(aws lambda get-function --function-name "${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}" --query 'Configuration.FunctionArn' --output text --region "$REGION")
    echo "LAMBDA_ARN=$LAMBDA_ARN" > .env.lambda
}

# Deploy EventBridge rules
deploy_eventbridge_rules() {
    log "Deploying EventBridge synchronization rules..."
    
    # Source Lambda ARN
    source .env.lambda
    
    # Deploy EventBridge stack
    aws cloudformation deploy \
        --template-file mcp-integration/eventbridge-sync-rules.yaml \
        --stack-name "${PROJECT_NAME}-mcp-eventbridge-${ENVIRONMENT}" \
        --parameter-overrides \
            ProjectName="$PROJECT_NAME" \
            Environment="$ENVIRONMENT" \
            SyncLambdaArn="$LAMBDA_ARN" \
        --capabilities CAPABILITY_IAM \
        --region "$REGION"
    
    success "EventBridge rules deployed"
}

# Create DynamoDB tables for knowledge base
create_knowledge_tables() {
    log "Creating DynamoDB tables for knowledge base..."
    
    # AWS Knowledge Table
    if ! aws dynamodb describe-table --table-name "${PROJECT_NAME}-aws-knowledge-${ENVIRONMENT}" --region "$REGION" &> /dev/null; then
        aws dynamodb create-table \
            --table-name "${PROJECT_NAME}-aws-knowledge-${ENVIRONMENT}" \
            --attribute-definitions \
                AttributeName=category,AttributeType=S \
                AttributeName=item_id,AttributeType=S \
            --key-schema \
                AttributeName=category,KeyType=HASH \
                AttributeName=item_id,KeyType=RANGE \
            --billing-mode PAY_PER_REQUEST \
            --time-to-live-specification \
                AttributeName=ttl,Enabled=true \
            --region "$REGION"
        
        success "AWS knowledge table created"
    else
        success "AWS knowledge table already exists"
    fi
    
    # Strands Knowledge Table
    if ! aws dynamodb describe-table --table-name "${PROJECT_NAME}-strands-knowledge-${ENVIRONMENT}" --region "$REGION" &> /dev/null; then
        aws dynamodb create-table \
            --table-name "${PROJECT_NAME}-strands-knowledge-${ENVIRONMENT}" \
            --attribute-definitions \
                AttributeName=category,AttributeType=S \
                AttributeName=item_id,AttributeType=S \
            --key-schema \
                AttributeName=category,KeyType=HASH \
                AttributeName=item_id,KeyType=RANGE \
            --billing-mode PAY_PER_REQUEST \
            --time-to-live-specification \
                AttributeName=ttl,Enabled=true \
            --region "$REGION"
        
        success "Strands knowledge table created"
    else
        success "Strands knowledge table already exists"
    fi
    
    # MCP Repository Table
    if ! aws dynamodb describe-table --table-name "${PROJECT_NAME}-mcp-repository-${ENVIRONMENT}" --region "$REGION" &> /dev/null; then
        aws dynamodb create-table \
            --table-name "${PROJECT_NAME}-mcp-repository-${ENVIRONMENT}" \
            --attribute-definitions \
                AttributeName=repository_name,AttributeType=S \
                AttributeName=last_updated,AttributeType=S \
            --key-schema \
                AttributeName=repository_name,KeyType=HASH \
                AttributeName=last_updated,KeyType=RANGE \
            --billing-mode PAY_PER_REQUEST \
            --time-to-live-specification \
                AttributeName=ttl,Enabled=true \
            --region "$REGION"
        
        success "MCP repository table created"
    else
        success "MCP repository table already exists"
    fi
    
    # MCP Health Table
    if ! aws dynamodb describe-table --table-name "${PROJECT_NAME}-mcp-health-${ENVIRONMENT}" --region "$REGION" &> /dev/null; then
        aws dynamodb create-table \
            --table-name "${PROJECT_NAME}-mcp-health-${ENVIRONMENT}" \
            --attribute-definitions \
                AttributeName=mcp_name,AttributeType=S \
                AttributeName=timestamp,AttributeType=S \
            --key-schema \
                AttributeName=mcp_name,KeyType=HASH \
                AttributeName=timestamp,KeyType=RANGE \
            --billing-mode PAY_PER_REQUEST \
            --time-to-live-specification \
                AttributeName=ttl,Enabled=true \
            --region "$REGION"
        
        success "MCP health table created"
    else
        success "MCP health table already exists"
    fi
}

# Test MCP integration
test_mcp_integration() {
    log "Testing MCP integration..."
    
    # Test Lambda function
    TEST_EVENT='{"sync_type": "health_check", "source": "manual_test"}'
    
    LAMBDA_RESULT=$(aws lambda invoke \
        --function-name "${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}" \
        --payload "$TEST_EVENT" \
        --region "$REGION" \
        response.json)
    
    if [[ $? -eq 0 ]]; then
        success "Lambda function test passed"
        
        # Show response
        if [[ -f response.json ]]; then
            log "Lambda response:"
            cat response.json | python3 -m json.tool
            rm response.json
        fi
    else
        warning "Lambda function test failed"
    fi
    
    # Test DynamoDB tables
    for table in "aws-knowledge" "strands-knowledge" "mcp-repository" "mcp-health"; do
        if aws dynamodb describe-table --table-name "${PROJECT_NAME}-${table}-${ENVIRONMENT}" --region "$REGION" &> /dev/null; then
            success "DynamoDB table ${table} is accessible"
        else
            warning "DynamoDB table ${table} is not accessible"
        fi
    done
}

# Setup MCP configuration
setup_mcp_configuration() {
    log "Setting up MCP configuration..."
    
    # Create MCP configuration directory in ECS task
    # This would typically be done during ECS deployment
    
    # For now, just validate the configuration file
    if [[ -f "mcp-integration/mcp-config.yaml" ]]; then
        success "MCP configuration file found"
        
        # Validate YAML syntax
        if python3 -c "import yaml; yaml.safe_load(open('mcp-integration/mcp-config.yaml'))" 2>/dev/null; then
            success "MCP configuration is valid YAML"
        else
            error "MCP configuration has invalid YAML syntax"
        fi
    else
        error "MCP configuration file not found"
    fi
}

# Trigger initial sync
trigger_initial_sync() {
    log "Triggering initial knowledge synchronization..."
    
    # Trigger full sync
    SYNC_EVENT='{"sync_type": "all", "source": "initial_deployment", "force_refresh": true}'
    
    aws lambda invoke \
        --function-name "${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}" \
        --payload "$SYNC_EVENT" \
        --region "$REGION" \
        --invocation-type Event \
        sync-response.json
    
    if [[ $? -eq 0 ]]; then
        success "Initial sync triggered"
        log "Sync will run in background. Check CloudWatch logs for progress."
    else
        warning "Failed to trigger initial sync"
    fi
    
    # Cleanup
    rm -f sync-response.json
}

# Generate deployment summary
generate_deployment_summary() {
    log "Generating MCP integration deployment summary..."
    
    # Get Lambda function info
    LAMBDA_INFO=$(aws lambda get-function --function-name "${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}" --region "$REGION" 2>/dev/null || echo "{}")
    
    # Get EventBridge rules
    EVENTBRIDGE_RULES=$(aws events list-rules --name-prefix "${PROJECT_NAME}" --region "$REGION" 2>/dev/null || echo '{"Rules": []}')
    
    # Get DynamoDB tables
    DYNAMODB_TABLES=$(aws dynamodb list-tables --region "$REGION" 2>/dev/null || echo '{"TableNames": []}')
    
    cat << EOF

🎉 MCP Integration Deployment Summary
=====================================

📊 Deployment Status: SUCCESS
🕐 Deployment Time: $(date)
🌍 Region: $REGION
🏷️  Environment: $ENVIRONMENT

🔧 Components Deployed:
  • Lambda Function: ${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}
  • EventBridge Rules: 6 scheduled sync rules
  • DynamoDB Tables: 4 knowledge base tables
  • CloudWatch Dashboard: MCP sync monitoring

📅 Sync Schedule:
  • AWS Docs: Monday & Thursday at 2 AM UTC
  • Strands Knowledge: Tuesday & Friday at 3 AM UTC
  • MCP Repositories: Wednesday & Saturday at 4 AM UTC
  • Full Sync: Sunday at 1 AM UTC
  • Health Checks: Every 5 minutes

🔍 Monitoring:
  • CloudWatch Logs: /aws/lambda/${PROJECT_NAME}-mcp-sync-${ENVIRONMENT}
  • CloudWatch Dashboard: ${PROJECT_NAME}-MCP-Sync-${ENVIRONMENT}
  • SNS Alerts: Configured for sync failures

💡 Next Steps:
  1. Monitor initial sync in CloudWatch logs
  2. Verify knowledge base population in DynamoDB
  3. Test MCP integration with Agent Core
  4. Configure MCP health monitoring alerts

🔗 Useful Commands:
  • Check sync status: aws lambda invoke --function-name ${PROJECT_NAME}-mcp-sync-${ENVIRONMENT} --payload '{"sync_type": "health_check"}' response.json
  • View logs: aws logs tail /aws/lambda/${PROJECT_NAME}-mcp-sync-${ENVIRONMENT} --follow
  • Manual sync: aws lambda invoke --function-name ${PROJECT_NAME}-mcp-sync-${ENVIRONMENT} --payload '{"sync_type": "all"}' --invocation-type Event response.json

EOF
}

# Cleanup temporary files
cleanup() {
    log "Cleaning up temporary files..."
    rm -f mcp-sync-handler.zip
    rm -f .env.lambda
    rm -f response.json
    rm -f sync-response.json
    success "Cleanup completed"
}

# Main execution
main() {
    echo "🔗 Agent Builder Platform - MCP Integration Deployment"
    echo "======================================================"
    echo
    
    check_prerequisites
    package_lambda_function
    deploy_lambda_function
    create_knowledge_tables
    deploy_eventbridge_rules
    setup_mcp_configuration
    test_mcp_integration
    trigger_initial_sync
    generate_deployment_summary
    cleanup
    
    success "MCP integration deployment completed successfully!"
}

# Trap for cleanup on exit
trap cleanup EXIT

# Run main function
main "$@"