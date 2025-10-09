#!/bin/bash

# Agent Builder Platform - AWS Connectivity Testing
# Test AWS connectivity and permissions without deploying resources

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[AWS-TEST]${NC} $1"; }
success() { echo -e "${GREEN}✅ $1${NC}"; }
failure() { echo -e "${RED}❌ $1${NC}"; }
warning() { echo -e "${YELLOW}⚠️  $1${NC}"; }

# Test AWS CLI and credentials
test_aws_credentials() {
    log "Testing AWS credentials and connectivity..."
    
    if ! command -v aws &> /dev/null; then
        failure "AWS CLI not installed"
        return 1
    fi
    
    # Test basic connectivity
    if aws sts get-caller-identity &> /dev/null; then
        local account_id=$(aws sts get-caller-identity --query Account --output text)
        local user_arn=$(aws sts get-caller-identity --query Arn --output text)
        success "AWS credentials valid"
        log "Account ID: $account_id"
        log "User/Role: $user_arn"
        
        # Store account ID for later use
        export AWS_ACCOUNT_ID="$account_id"
    else
        failure "AWS credentials invalid or not configured"
        return 1
    fi
}

# Test Bedrock access (critical for AI consultants)
test_bedrock_access() {
    log "Testing Amazon Bedrock access..."
    
    local region=${AWS_REGION:-us-east-1}
    
    if aws bedrock list-foundation-models --region "$region" &> /dev/null; then
        success "Bedrock access available in $region"
        
        # Check for Claude 3 Haiku specifically
        if aws bedrock list-foundation-models --region "$region" \
           --query 'modelSummaries[?contains(modelId, `claude-3-haiku`)]' \
           --output text | grep -q claude; then
            success "Claude 3 Haiku model available"
        else
            warning "Claude 3 Haiku model may not be available"
            log "Available models:"
            aws bedrock list-foundation-models --region "$region" \
                --query 'modelSummaries[].modelId' --output text | head -5
        fi
    else
        failure "Bedrock access not available in $region"
        warning "Bedrock is required for AI consultants"
        return 1
    fi
}

# Test required AWS service availability
test_service_availability() {
    log "Testing AWS service availability..."
    
    local region=${AWS_REGION:-us-east-1}
    local services_available=true
    
    # Test ECS
    if aws ecs list-clusters --region "$region" &> /dev/null; then
        success "ECS service available"
    else
        failure "ECS service not available"
        services_available=false
    fi
    
    # Test S3
    if aws s3 ls &> /dev/null; then
        success "S3 service available"
    else
        failure "S3 service not available"
        services_available=false
    fi
    
    # Test DynamoDB
    if aws dynamodb list-tables --region "$region" &> /dev/null; then
        success "DynamoDB service available"
    else
        failure "DynamoDB service not available"
        services_available=false
    fi
    
    # Test CloudFormation
    if aws cloudformation list-stacks --region "$region" &> /dev/null; then
        success "CloudFormation service available"
    else
        failure "CloudFormation service not available"
        services_available=false
    fi
    
    if ! $services_available; then
        failure "Some required AWS services are not available"
        return 1
    fi
}

# Test IAM permissions (simulate without creating resources)
test_iam_permissions() {
    log "Testing IAM permissions..."
    
    local region=${AWS_REGION:-us-east-1}
    local permissions_ok=true
    
    # Test S3 permissions
    if aws iam simulate-principal-policy \
       --policy-source-arn $(aws sts get-caller-identity --query Arn --output text) \
       --action-names s3:CreateBucket s3:PutObject s3:GetObject \
       --resource-arns "arn:aws:s3:::test-bucket" "arn:aws:s3:::test-bucket/*" \
       --query 'EvaluationResults[?Decision!=`allowed`]' \
       --output text | grep -q .; then
        warning "Some S3 permissions may be missing"
    else
        success "S3 permissions appear sufficient"
    fi
    
    # Test DynamoDB permissions
    if aws iam simulate-principal-policy \
       --policy-source-arn $(aws sts get-caller-identity --query Arn --output text) \
       --action-names dynamodb:CreateTable dynamodb:PutItem dynamodb:GetItem \
       --resource-arns "arn:aws:dynamodb:$region:$AWS_ACCOUNT_ID:table/test-table" \
       --query 'EvaluationResults[?Decision!=`allowed`]' \
       --output text | grep -q .; then
        warning "Some DynamoDB permissions may be missing"
    else
        success "DynamoDB permissions appear sufficient"
    fi
    
    # Test ECS permissions
    if aws iam simulate-principal-policy \
       --policy-source-arn $(aws sts get-caller-identity --query Arn --output text) \
       --action-names ecs:CreateCluster ecs:CreateService \
       --resource-arns "*" \
       --query 'EvaluationResults[?Decision!=`allowed`]' \
       --output text | grep -q .; then
        warning "Some ECS permissions may be missing"
    else
        success "ECS permissions appear sufficient"
    fi
    
    # Test Bedrock permissions
    if aws iam simulate-principal-policy \
       --policy-source-arn $(aws sts get-caller-identity --query Arn --output text) \
       --action-names bedrock:InvokeModel bedrock:ListFoundationModels \
       --resource-arns "*" \
       --query 'EvaluationResults[?Decision!=`allowed`]' \
       --output text | grep -q .; then
        warning "Some Bedrock permissions may be missing"
    else
        success "Bedrock permissions appear sufficient"
    fi
}

# Test CloudFormation template validation
test_template_validation() {
    log "Testing CloudFormation template validation..."
    
    local region=${AWS_REGION:-us-east-1}
    
    if aws cloudformation validate-template \
       --template-body file://infrastructure/main-stack.yaml \
       --region "$region" &> /dev/null; then
        success "CloudFormation template is valid"
        
        # Get template summary
        local resources=$(aws cloudformation validate-template \
                         --template-body file://infrastructure/main-stack.yaml \
                         --region "$region" \
                         --query 'length(Parameters)' --output text)
        log "Template has $resources parameters"
    else
        failure "CloudFormation template validation failed"
        aws cloudformation validate-template \
            --template-body file://infrastructure/main-stack.yaml \
            --region "$region" 2>&1 | head -10
        return 1
    fi
}

# Test cost estimation
test_cost_estimation() {
    log "Estimating deployment costs..."
    
    local region=${AWS_REGION:-us-east-1}
    
    # Get current billing information
    if aws ce get-cost-and-usage \
       --time-period Start=$(date -u -d '1 day ago' +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
       --granularity DAILY \
       --metrics BlendedCost \
       --region us-east-1 &> /dev/null; then
        
        local current_cost=$(aws ce get-cost-and-usage \
                           --time-period Start=$(date -u -d '1 day ago' +%Y-%m-%d),End=$(date -u +%Y-%m-%d) \
                           --granularity DAILY \
                           --metrics BlendedCost \
                           --region us-east-1 \
                           --query 'ResultsByTime[0].Total.BlendedCost.Amount' \
                           --output text 2>/dev/null || echo "0")
        
        success "Current daily cost: \$${current_cost}"
        
        if (( $(echo "$current_cost > 5" | bc -l) )); then
            warning "Current costs are already above \$5/day"
            warning "Monitor costs carefully during deployment"
        else
            success "Current costs are low - good for hackathon budget"
        fi
    else
        warning "Cannot access cost information (may require billing permissions)"
    fi
}

# Test free tier status
test_free_tier_status() {
    log "Checking AWS free tier status..."
    
    # Check if account is eligible for free tier
    local account_age=$(aws support describe-trusted-advisor-checks \
                       --language en \
                       --query 'checks[?name==`Service Limits`].id' \
                       --output text 2>/dev/null || echo "unknown")
    
    if [[ "$account_age" != "unknown" ]]; then
        success "Account has access to support API"
        log "Free tier eligibility can be checked in AWS Console"
    else
        warning "Cannot check free tier status programmatically"
        log "Check free tier usage in AWS Billing Console"
    fi
    
    # Provide free tier guidance
    log "Free tier limits relevant to this project:"
    log "  • ECS Fargate: 20 GB-hours per month"
    log "  • DynamoDB: 25 GB storage, 25 WCU, 25 RCU"
    log "  • S3: 5 GB storage, 20,000 GET requests"
    log "  • Lambda: 1M requests, 400,000 GB-seconds"
    log "  • CloudWatch: 5 GB log ingestion"
}

# Test region optimization
test_region_optimization() {
    log "Testing region optimization..."
    
    local current_region=${AWS_REGION:-$(aws configure get region)}
    local recommended_region="us-east-1"
    
    if [[ "$current_region" == "$recommended_region" ]]; then
        success "Using recommended region: $current_region"
    else
        warning "Current region: $current_region"
        warning "Recommended region: $recommended_region (best Bedrock availability)"
    fi
    
    # Test Bedrock availability in current region
    if aws bedrock list-foundation-models --region "$current_region" &> /dev/null; then
        success "Bedrock available in current region"
    else
        failure "Bedrock not available in current region"
        log "Consider switching to us-east-1 for best service availability"
    fi
}

# Generate connectivity test report
generate_connectivity_report() {
    echo
    echo "🔗 AWS Connectivity Test Report"
    echo "==============================="
    echo
    echo "✅ Completed Tests:"
    echo "  • AWS credentials and connectivity"
    echo "  • Amazon Bedrock access (AI consultants)"
    echo "  • Required AWS service availability"
    echo "  • IAM permissions simulation"
    echo "  • CloudFormation template validation"
    echo "  • Cost estimation and free tier status"
    echo "  • Region optimization"
    echo
    echo "🎯 Key Findings:"
    echo "  • Account ID: ${AWS_ACCOUNT_ID:-unknown}"
    echo "  • Region: ${AWS_REGION:-$(aws configure get region)}"
    echo "  • Bedrock Access: $(aws bedrock list-foundation-models --region ${AWS_REGION:-us-east-1} &>/dev/null && echo "✅ Available" || echo "❌ Not Available")"
    echo "  • Template Status: $(aws cloudformation validate-template --template-body file://infrastructure/main-stack.yaml --region ${AWS_REGION:-us-east-1} &>/dev/null && echo "✅ Valid" || echo "❌ Invalid")"
    echo
    echo "💰 Cost Considerations:"
    echo "  • Estimated daily cost: \$0.50 - \$2.00"
    echo "  • Hackathon total: \$3.00 - \$14.00"
    echo "  • Primary cost: Bedrock (AI consultants)"
    echo
    echo "🚀 Deployment Readiness:"
    if aws sts get-caller-identity &>/dev/null && \
       aws bedrock list-foundation-models --region ${AWS_REGION:-us-east-1} &>/dev/null && \
       aws cloudformation validate-template --template-body file://infrastructure/main-stack.yaml --region ${AWS_REGION:-us-east-1} &>/dev/null; then
        echo "  ✅ Ready for AWS deployment"
        echo
        echo "Next Steps:"
        echo "  1. Run './scripts/deploy-infrastructure.sh'"
        echo "  2. Monitor costs in AWS Billing Dashboard"
        echo "  3. Set up billing alerts if not already configured"
    else
        echo "  ❌ Not ready for deployment"
        echo
        echo "Required Actions:"
        echo "  1. Fix any failed tests above"
        echo "  2. Ensure Bedrock access is available"
        echo "  3. Verify CloudFormation template is valid"
        echo "  4. Re-run this test script"
    fi
}

# Main execution
main() {
    echo "🔗 Agent Builder Platform - AWS Connectivity Testing"
    echo "===================================================="
    echo
    echo "Testing AWS connectivity and permissions..."
    echo "This test does not create any AWS resources or incur costs."
    echo
    
    test_aws_credentials
    test_bedrock_access
    test_service_availability
    test_iam_permissions
    test_template_validation
    test_cost_estimation
    test_free_tier_status
    test_region_optimization
    
    generate_connectivity_report
}

# Run tests
main "$@"