#!/bin/bash

# Deploy CloudFront CDN for Agent Builder Platform
# Requirements: 12.2

set -e

# Configuration
PROJECT_NAME="${PROJECT_NAME:-agent-builder}"
ENVIRONMENT="${ENVIRONMENT:-dev}"
REGION="${AWS_REGION:-us-east-1}"
STACK_NAME="${PROJECT_NAME}-${ENVIRONMENT}-cdn"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}Deploying CloudFront CDN${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Project: $PROJECT_NAME"
echo "Environment: $ENVIRONMENT"
echo "Region: $REGION"
echo "Stack: $STACK_NAME"
echo ""

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo -e "${RED}Error: AWS CLI is not installed${NC}"
    exit 1
fi

# Check if frontend bucket exists
FRONTEND_BUCKET="${PROJECT_NAME}-${ENVIRONMENT}-frontend"
if ! aws s3 ls "s3://${FRONTEND_BUCKET}" &> /dev/null; then
    echo -e "${YELLOW}Warning: Frontend bucket does not exist. Creating...${NC}"
    aws s3 mb "s3://${FRONTEND_BUCKET}" --region "$REGION"
    
    # Enable static website hosting
    aws s3 website "s3://${FRONTEND_BUCKET}" \
        --index-document index.html \
        --error-document index.html
fi

# Check if logs bucket exists
LOGS_BUCKET="${PROJECT_NAME}-${ENVIRONMENT}-logs"
if ! aws s3 ls "s3://${LOGS_BUCKET}" &> /dev/null; then
    echo -e "${YELLOW}Warning: Logs bucket does not exist. Creating...${NC}"
    aws s3 mb "s3://${LOGS_BUCKET}" --region "$REGION"
fi

# Deploy CloudFormation stack
echo -e "${GREEN}Deploying CloudFormation stack...${NC}"
aws cloudformation deploy \
    --template-file infrastructure/cloudfront-cdn.yaml \
    --stack-name "$STACK_NAME" \
    --parameter-overrides \
        ProjectName="$PROJECT_NAME" \
        Environment="$ENVIRONMENT" \
        FrontendBucketName="$FRONTEND_BUCKET" \
    --capabilities CAPABILITY_NAMED_IAM \
    --region "$REGION" \
    --no-fail-on-empty-changeset

# Get CloudFront distribution ID
DISTRIBUTION_ID=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`DistributionId`].OutputValue' \
    --output text)

# Get CloudFront domain name
DISTRIBUTION_DOMAIN=$(aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query 'Stacks[0].Outputs[?OutputKey==`DistributionDomainName`].OutputValue' \
    --output text)

echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}CDN Deployment Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Distribution ID: $DISTRIBUTION_ID"
echo "Distribution Domain: $DISTRIBUTION_DOMAIN"
echo "Frontend URL: https://$DISTRIBUTION_DOMAIN"
echo ""
echo -e "${YELLOW}Note: CloudFront distribution may take 15-20 minutes to fully deploy${NC}"
echo ""

# Save outputs to file
cat > cdn-outputs.json <<EOF
{
  "distributionId": "$DISTRIBUTION_ID",
  "distributionDomain": "$DISTRIBUTION_DOMAIN",
  "frontendUrl": "https://$DISTRIBUTION_DOMAIN",
  "frontendBucket": "$FRONTEND_BUCKET"
}
EOF

echo -e "${GREEN}Outputs saved to cdn-outputs.json${NC}"
